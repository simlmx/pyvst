from ctypes import (cdll, Structure, POINTER, CFUNCTYPE,
                    c_void_p, c_int, c_float, c_int32, c_double, c_char,
                    addressof, byref, pointer)
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
        raise NotImplementedError('audio master call back opcode "{opcode}" not supported yet'.format(opcode=opcode))


class VstPlugin:
    def __init__(self, filename):
        self._lib = cdll.LoadLibrary(filename)
        self._lib.VSTPluginMain.argtypes = [AUDIO_MASTER_CALLBACK_TYPE]
        self._lib.VSTPluginMain.restype = POINTER(AEffect)
        self._effect = self._lib.VSTPluginMain(AUDIO_MASTER_CALLBACK_TYPE(_audio_master_callback)).contents

        assert self._effect.magic == MAGIC

        if self.vst_version != 2400:
            print('Warning: this plugin is not a VST2.4 plugin')

    def _dispatch(self, opcode, index=0, value=0, ptr=None, opt=0.):
        if ptr is None:
            ptr = c_void_p(None)
        # self._effect.dispatcher.argtypes = [POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float]
        output = self._effect.dispatcher(byref(self._effect), c_int32(opcode), c_int32(index), c_int(value), ptr, c_float(opt))
        return output

    # Parameters
    #
    def _get_param_attr(self, index, opcode):
        p_char = pointer(c_char())
        self._dispatch(opcode, index=index, ptr=p_char)
        name = ''
        for i in range(VstStringConstants.kVstMaxParamStrLen):
            char = p_char[i]
            if char:
                name += char.decode()
            else:
                break
        return name

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
        p = pointer(VstParameterProperties())
        self._dispatch(AEffectOpcodes.effGetParameterProperties, index=index, ptr=p)
        return p.contents

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
        ptr = pointer(VstPinProperties())
        is_supported = self._dispatch(AEffectOpcodes.effGetInputProperties, index=index, ptr=ptr)
        ret = ptr.contents
        ret.is_supported = is_supported
        return ret

    def get_output_properties(self, index):
        ptr = pointer(VstPinProperties())
        is_supported = self._dispatch(AEffectOpcodes.effGetOutputProperties, index=index, ptr=ptr)
        ret = ptr.contents
        ptr.is_supported = is_supported
        return ret

    @property
    def plug_category(self):
        return VstPlugCategory(self._dispatch(AEffectOpcodes.effGetPlugCategory))

    # Processing
    #
    def process_events(self, vst_events):
        self._dispatch(AEffectOpcodes.effProcessEvents, ptr=byref(vst_events))


    #
    def __getattr__(self, attr):
        """We also try getattr(self._effect, attr) so we don't have to wrap all of those."""
        try:
            return getattr(self._effect, attr)
        except AttributeError:
            pass
        raise AttributeError('object VstPlugin has no attribute "{0}" and effect has no attribute "{0}'.format(attr))
