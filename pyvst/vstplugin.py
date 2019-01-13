import contextlib
from ctypes import (cdll, POINTER, c_double,
                    c_void_p, c_int, c_float, c_int32,
                    byref, string_at, create_string_buffer)
from warnings import warn

import numpy
from wurlitzer import pipes

from .vstwrap import (
    AudioMasterOpcodes,
    AEffect,
    AEffectOpcodes,
    AUDIO_MASTER_CALLBACK_TYPE,
    VstPinProperties,
    VstParameterProperties,
    VstPlugCategory,
    VstAEffectFlags,
)


# define kEffectMagic CCONST ('V', 's', 't', 'P')
# or: MAGIC = int.from_bytes(b'VstP', 'big')
MAGIC = 1450406992


def _default_audio_master_callback(effect, opcode, *args):
    """Version naive audio master callback. This mimicks more than minimal host."""
    if opcode == AudioMasterOpcodes.audioMasterVersion:
        return 2400
    return 0


class VstPlugin:
    def __init__(self, filename, audio_master_callback=None, verbose=False):
        """
        :param verbose: Set to True to show the plugin's stdout/stderr. By default (False),
            we capture it.
        """
        self.verbose = verbose

        if audio_master_callback is None:
            audio_master_callback = _default_audio_master_callback
        self._lib = cdll.LoadLibrary(filename)
        self._lib.VSTPluginMain.argtypes = [AUDIO_MASTER_CALLBACK_TYPE]
        self._lib.VSTPluginMain.restype = POINTER(AEffect)

        with pipes() if not verbose else contextlib.suppress():
            self._effect = self._lib.VSTPluginMain(AUDIO_MASTER_CALLBACK_TYPE(
                audio_master_callback)).contents

        assert self._effect.magic == MAGIC

        if self.vst_version != 2400:
            warn('This plugin is not a VST2.4 plugin.')

    def open(self):
        self._dispatch(AEffectOpcodes.effOpen)

    def close(self):
        self._dispatch(AEffectOpcodes.effClose)

    def resume(self):
        self._dispatch(AEffectOpcodes.effMainsChanged, value=1)

    def suspend(self):
        self._dispatch(AEffectOpcodes.effMainsChanged, value=0)

    def __del__(self):
        # This seem to fix segmentation faults when the VstPlugin is garbage collected.
        self.suspend()
        self.close()

    def _dispatch(self, opcode, index=0, value=0, ptr=None, opt=0.):
        if ptr is None:
            ptr = c_void_p(None)
        # self._effect.dispatcher.argtypes = [POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float]

        # That `pipes()` caused a lot of issues for some reason.
        # with pipes() if not self.verbose and contextlib.suppress():
        output = self._effect.dispatcher(byref(self._effect), c_int32(opcode), c_int32(index),
                                         c_int(value), ptr, c_float(opt))
        return output

    # Parameters
    #
    @property
    def num_params(self):
        return self._effect.num_params

    def _get_param_attr(self, index, opcode):
        # It should be VstStringConstants.kVstMaxParamStrLen == 8 but I've encountered some VST
        # with more that would segfault.
        buf = create_string_buffer(64)
        self._dispatch(opcode, index=index, ptr=byref(buf))
        return string_at(buf).decode()

    def get_param_name(self, index):
        return self._get_param_attr(index, AEffectOpcodes.effGetParamName)

    def get_param_label(self, index):
        return self._get_param_attr(index, AEffectOpcodes.effGetParamLabel)

    def get_param_display(self, index):
        return self._get_param_attr(index, AEffectOpcodes.effGetParamDisplay)

    def get_param_value(self, index):
        return self._effect.get_parameter(byref(self._effect), c_int(index))

    def set_param_value(self, index, value):
        self._effect.set_parameter(byref(self._effect), index, value)

    def get_param_properties(self, index):
        props = VstParameterProperties()
        self._dispatch(AEffectOpcodes.effGetParameterProperties, index=index, ptr=byref(props))
        return props

    @property
    def vst_version(self):
        return self._dispatch(AEffectOpcodes.effGetVstVersion)

    @property
    def num_inputs(self):
        return self._effect.num_inputs

    @property
    def num_outputs(self):
        return self._effect.num_outputs

    @property
    def num_midi_in(self):
        return self._dispatch(AEffectOpcodes.effGetNumMidiInputChannels)

    @property
    def num_midi_out(self):
        return self._dispatch(AEffectOpcodes.effGetNumMidiOutputChannels)

    def get_input_properties(self, index):
        props = VstPinProperties()
        is_supported = self._dispatch(AEffectOpcodes.effGetInputProperties, index=index,
                                      ptr=byref(props))
        props.is_supported = is_supported
        return props

    def get_output_properties(self, index):
        props = VstPinProperties()
        is_supported = self._dispatch(AEffectOpcodes.effGetOutputProperties, index=index, ptr=byref(props))
        props.is_supported = is_supported
        return props

    @property
    def plug_category(self):
        return VstPlugCategory(self._dispatch(AEffectOpcodes.effGetPlugCategory))

    # Processing
    #
    def _make_empty_array(self, sample_frames, num_chan, c_type):
        """Initializes a pointer of pointer array."""
        p_type = POINTER(c_type)

        out = (p_type * num_chan)(*[(c_type * sample_frames)() for i in range(num_chan)])
        for i in range(num_chan):
            out[i] = (c_type * sample_frames)()
        return out

    def process(self, input=None, sample_frames=None, double=None):

        if double is None:
            if self.can_double_replacing:
                double = True

        if double:
            c_type = c_double
            process_fn = self._effect.process_double_replacing
        else:
            c_type = c_float
            process_fn = self._effect.process_replacing

        if input is None:
            input = self._make_empty_array(sample_frames, self.num_inputs, c_type)
        else:
            input = (POINTER(c_type) * self.num_inputs)(*[row.ctypes.data_as(POINTER(c_type)) for row in input])

        if sample_frames is None:
            raise ValueError('You must provide `sample_frames` when there is no input')

        output = self._make_empty_array(sample_frames, self.num_outputs, c_type)

        with pipes() if not self.verbose else contextlib.suppress():
            process_fn(
                byref(self._effect),
                input,
                output,
                sample_frames
            )

        output = numpy.vstack([numpy.ctypeslib.as_array(output[i], shape=(sample_frames,))
                               for i in range(self.num_outputs)])
        return output

    def process_events(self, vst_events):
        self._dispatch(AEffectOpcodes.effProcessEvents, ptr=byref(vst_events))

    def set_block_size(self, max_block_size):
        self._dispatch(AEffectOpcodes.effSetBlockSize, value=max_block_size)

    def set_sample_rate(self, sample_rate):
        self._dispatch(AEffectOpcodes.effSetSampleRate, opt=sample_rate)

    @property
    def is_synth(self):
        return self._effect.flags & VstAEffectFlags.effFlagsIsSynth

    @property
    def can_double_replacing(self):
        return self._effect.flags & VstAEffectFlags.effFlagsCanDoubleReplacing
