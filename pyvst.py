from ctypes import cdll, Structure, POINTER, CFUNCTYPE, c_void_p, c_int, c_float, byref, c_int32, c_double, c_char
from enum import Enum


# define kEffectMagic CCONST ('V', 's', 't', 'P')
MAGIC = 1450406992


class AudioMasterOpcodes(Enum):
    # [index]: parameter index [opt]: parameter value  @see AudioEffect::setParameterAutomated
    audioMasterAutomate = 0
    # [return value]: Host VST version (for example 2400 for VST 2.4) @see AudioEffect::getMasterVersion
    audioMasterVersion = 1
    # [return value]: current unique identifier on shell plug-in  @see AudioEffect::getCurrentUniqueId
    audioMasterCurrentId = 2
    # no arguments  @see AudioEffect::masterIdle
    audioMasterIdle = 3


class AEffect(Structure):
    pass


# FIXME TO CAPS? or wrap into class? private?
audio_master_callback_type = CFUNCTYPE(c_void_p, POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float)
# typedef VstIntPtr (VSTCALLBACK *AEffectDispatcherProc) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
AEFFECT_DISPATCHER_PROC_TYPE = CFUNCTYPE(c_int, POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float)
# typedef void (VSTCALLBACK *AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sampleFrames);
# AEFFECT_PROCESS_PROC_TYPE = CFUNCTYPE(c_void_p,
#                                       POINTER(AEffect),
#                                       POINTER(POINTER(c_float)),
#                                       POINTER(POINTER(c_float)),
#                                       c_int32,)
get_parameter_type = CFUNCTYPE(c_float, POINTER(AEffect), c_int32)
set_parameter_type = CFUNCTYPE(c_void_p, POINTER(AEffect), c_int32, c_float)
# typedef void (VSTCALLBACK *AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sampleFrames);
_AEFFECT_PROCESS_PROC = CFUNCTYPE(c_void_p, POINTER(AEffect), POINTER(POINTER(c_float)), POINTER(POINTER(c_float)), c_int32)
# typedef void (VSTCALLBACK *AEffectProcessDoubleProc) (AEffect* effect, double** inputs, double** outputs, VstInt32 sampleFrames);
_AEFFECT_PROCESS_DOUBLE_PROC = CFUNCTYPE(c_void_p, POINTER(AEffect), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), c_int32)


AEffect._fields_ = [
    ('magic', c_int32),
    ('dispatcher', AEFFECT_DISPATCHER_PROC_TYPE),
    ('_process', c_void_p),
    ('set_parameter', set_parameter_type),
    ('get_parameter', get_parameter_type),
    ('num_programs', c_int32),
    ('num_params', c_int32),
    ('num_inputs', c_int32),
    ('num_outputs', c_int32),
    ('flags', c_int32),
    ('resvd1', c_int),
    ('resvd2', c_int),
    ('initial_delay', c_int32),
    ('_realQualities', c_int32),
    ('_offQualities', c_int32),
    ('_ioRatio', c_int32),
    ('object', c_void_p),
    ('user', c_void_p),
    ('unique_id', c_int32),
    ('version', c_int32),
    ('process_replacing', _AEFFECT_PROCESS_PROC),
    ('process_double_replacing', _AEFFECT_PROCESS_DOUBLE_PROC),
    ('_future1', c_char * 56),
    ('_future2', c_char * 60),
    ('patate', c_int * 100)
]


def audio_master_callback(effect, opcode, index, value, ptr, opt):
    if opcode == AudioMasterOpcodes.audioMasterVersion.value:
        return 2400
    else:
        raise NotImplementedError('audio master call back opcode "{opcode}" not supported yet'.format(opcode=opcode))


class VstPlugin:
    def __init__(self, filename):
        self._lib = cdll.LoadLibrary(filename)
        self._lib.VSTPluginMain.argtypes = [audio_master_callback_type]
        self._lib.VSTPluginMain.restype = POINTER(AEffect)
        self._effect = self._lib.VSTPluginMain(audio_master_callback_type(audio_master_callback)).contents

        assert self._effect.magic == MAGIC

    def _dispatch(self, opcode, index=0, value=0, ptr=None, opt=0.):
        if ptr is None:
            ptr = c_void_p(None)
        # self._effect.dispatcher.argtypes = [POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float]
        self._effect.dispatcher(byref(self._effect), c_int32(opcode), c_int32(index), c_int(value), ptr, c_float(opt))
        return output

    def get_parameter(self, i):
        # self._effect.get_parameter.restype = c_void_p
        # self._effect.get_parameter.argtypes = [POINTER(AEffect), c_int]
        value = self._effect.get_parameter(byref(self._effect), c_int(i))
        return value

    def set_parameter(self, index, value):
        # self._effect.set_parameter.restype = c_void_p
        # self._effect.set_parameter.argtypes = [POINTER(AEffect), c_int, c_float]
        self._effect.set_parameter(byref(self._effect), index, value)

    def __getattr__(self, attr):
        """We also try getattr(self._effect, attr) so we don't have to wrap all of those."""
        try:
            return getattr(self._effect, attr)
        except AttributeError:
            pass
        raise AttributeError('object VstPlugin has no attribute "{0}" and effect has no attribute "{0}'.format(attr))
