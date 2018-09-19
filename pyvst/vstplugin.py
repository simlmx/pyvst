from ctypes import (cdll, Structure, POINTER, CFUNCTYPE,
                    c_void_p, c_int, c_float, c_int32, c_double, c_char,
                    addressof, byref, pointer, cast, string_at, create_string_buffer)

import numpy

from .vstwrap import (
    AudioMasterOpcodes,
    AEffect,
    AEffectOpcodes,
    AUDIO_MASTER_CALLBACK_TYPE,
    VstStringConstants,
    VstPinProperties,
    VstParameterProperties,
    VstPlugCategory,
)


# define kEffectMagic CCONST ('V', 's', 't', 'P')
# or: MAGIC = int.from_bytes(b'VstP', 'big')
MAGIC = 1450406992


def _audio_master_callback(effect, opcode, index, value, ptr, opt):
    if opcode == AudioMasterOpcodes.audioMasterVersion.value:
        return 2400
    else:
        print('WARNING: audio master call back opcode "{}" not supported yet'.format(opcode))
        return 0

class VstPlugin:
    def __init__(self, filename):
        self._lib = cdll.LoadLibrary(filename)
        self._lib.VSTPluginMain.argtypes = [AUDIO_MASTER_CALLBACK_TYPE]
        self._lib.VSTPluginMain.restype = POINTER(AEffect)
        self._effect = self._lib.VSTPluginMain(AUDIO_MASTER_CALLBACK_TYPE(_audio_master_callback)).contents

        assert self._effect.magic == MAGIC

        if self.vst_version != 2400:
            print('Warning: this plugin is not a VST2.4 plugin')

    def open(self):
        self._dispatch(AEffectOpcodes.effOpen)

    def close(self):
        self._dispatch(AEffectOpcodes.effClose)

    def resume(self):
        self._dispatch(AEffectOpcodes.effMainsChanged, value=1)

    def suspend(self):
        self._dispatch(AEffectOpcodes.effMainsChanged, value=0)

    def _dispatch(self, opcode, index=0, value=0, ptr=None, opt=0.):
        if ptr is None:
            ptr = c_void_p(None)
        # self._effect.dispatcher.argtypes = [POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float]
        output = self._effect.dispatcher(byref(self._effect), c_int32(opcode), c_int32(index), c_int(value), ptr, c_float(opt))
        return output

    # Parameters
    #
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
    def _make_array(self, sample_frames, num_chan):
        p_float = POINTER(c_float)

        out = (p_float * num_chan)(*[(c_float * sample_frames)() for i in range(num_chan)])
        for i in range(num_chan):
            out[i] = (c_float * sample_frames)()
        return out

    def process(self, input=None, sample_frames=None):
        if input is None:
            input = self._make_array(sample_frames, self.num_inputs)
        else:
            raise NotImplementedError(
                'We only support VstI for the moment so there should be no audio input')

        if sample_frames is None:
            raise ValueError('You must provide `sample_frames` where there is no input')

        output = self._make_array(sample_frames, self.num_outputs)

        self._effect.process_replacing(
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

    #
    def __getattr__(self, attr):
        """We also try getattr(self._effect, attr) so we don't have to wrap all of those."""
        try:
            return getattr(self._effect, attr)
        except AttributeError:
            pass
        raise AttributeError('object VstPlugin has no attribute "{0}" and effect has no attribute "{0}'.format(attr))
