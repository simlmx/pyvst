from ctypes import (cdll, Structure, POINTER, CFUNCTYPE,
                    c_void_p, c_int, c_float, c_int32, c_double, c_char,
                    addressof, byref, pointer)
from enum import IntEnum


# define kEffectMagic CCONST ('V', 's', 't', 'P')
MAGIC = 1450406992


class AudioMasterOpcodes(IntEnum):
    # [index]: parameter index [opt]: parameter value  @see AudioEffect::setParameterAutomated
    audioMasterAutomate = 0
    # [return value]: Host VST version (for example 2400 for VST 2.4) @see AudioEffect::getMasterVersion
    audioMasterVersion = 1
    # [return value]: current unique identifier on shell plug-in  @see AudioEffect::getCurrentUniqueId
    audioMasterCurrentId = 2
    # no arguments  @see AudioEffect::masterIdle
    audioMasterIdle = 3


class AEffectOpcodes(IntEnum):
    # no arguments  @see AudioEffect::open
    effOpen = 0
    # no arguments  @see AudioEffect::close
    effClose = 1

    # [value]: new program number  @see AudioEffect::setProgram
    effSetProgram = 2
    # [return value]: current program number  @see AudioEffect::getProgram
    effGetProgram = 3
    # [ptr]: char* with new program name, limited to #kVstMaxProgNameLen  @see AudioEffect::setProgramName
    effSetProgramName = 4
    # [ptr]: char buffer for current program name, limited to #kVstMaxProgNameLen  @see AudioEffect::getProgramName
    effGetProgramName = 5

    # [ptr]: char buffer for parameter label, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterLabel
    effGetParamLabel = 6
    # [ptr]: char buffer for parameter display, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterDisplay
    effGetParamDisplay = 7
    # [ptr]: char buffer for parameter name, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterName
    effGetParamName = 8
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetVu)

    # [opt]: new sample rate for audio processing  @see AudioEffect::setSampleRate
    effSetSampleRate = 10
    # [value]: new maximum block size for audio processing  @see AudioEffect::setBlockSize
    effSetBlockSize = 11
    # [value]: 0 means "turn off", 1 means "turn on"  @see AudioEffect::suspend @see AudioEffect::resume
    effMainsChanged = 12

    # [ptr]: #ERect** receiving pointer to editor size  @see ERect @see AEffEditor::getRect
    effEditGetRect = 13
    # [ptr]: system dependent Window pointer, e.g. HWND on Windows  @see AEffEditor::open
    effEditOpen = 14
    # no arguments @see AEffEditor::close
    effEditClose = 15

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effEditDraw)
    # deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effEditMouse)
    # deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effEditKey)

    # no arguments @see AEffEditor::idle
    effEditIdle = 19

    # deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effEditTop)
    # deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effEditSleep)
    # deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effIdentify)

    # [ptr]: void** for chunk data address [index]: 0 for bank, 1 for program  @see AudioEffect::getChunk
    effGetChunk = 23
    # [ptr]: chunk data [value]: byte size [index]: 0 for bank, 1 for program  @see AudioEffect::setChunk
    effSetChunk = 24

    effNumOpcodes = 25


class VstStringConstants:
    # used for #effGetProgramName, #effSetProgramName, #effGetProgramNameIndexed
    kVstMaxProgNameLen   = 24
    # used for #effGetParamLabel, #effGetParamDisplay, #effGetParamName
    kVstMaxParamStrLen   = 8
    # used for #effGetVendorString, #audioMasterGetVendorString
    kVstMaxVendorStrLen  = 64
    # used for #effGetProductString, #audioMasterGetProductString
    kVstMaxProductStrLen = 64
    # used for #effGetEffectName
    kVstMaxEffectNameLen = 32


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


class VstParameterProperties(Structure):
    _fields_ = [
        ('step_float', c_float),
        ('small_step_float', c_float),
        ('large_step_float', c_float),
        ('label', c_char * 64),  # FIXME remove hard-coded 64
        ('flags', c_int32),
        ('min_int', c_int32),
        ('max_int', c_int32),
        ('step_int', c_int32),
        ('large_step_int', c_int32),
        ('short_label', c_char * 8),  # FIXME same
        # FIXME unfinished
    ]


class VstPinProperties(Structure):
    _fields_ = [
        # pin name
        ('label', c_char * 64),  # FIXME same
        # VstPinPropertiesFlags
        ('flags', c_int32),
        # VstSpeakerArrangementType
        ('arrangement_type', c_int32),
        # short name (recommende 6 + delimiter)
        ('short_label', c_char * 8),  # FIXME same
    ]


def audio_master_callback(effect, opcode, index, value, ptr, opt):
    if opcode == AudioMasterOpcodes.audioMasterVersion.value:
        return 2400
    else:
        raise NotImplementedError('audio master call back opcode "{opcode}" not supported yet'.format(opcode=opcode))


# class Parameter:
#     def __init__(self, name, label, value, display):
#         self.name = name
#         self.label = label
#         self.value = value
#         self.display = display

#     def __str__(self):
#         return '{}={}'.format(self.name, self.label)


class VstPlugin:
    def __init__(self, filename):
        self._lib = cdll.LoadLibrary(filename)
        self._lib.VSTPluginMain.argtypes = [audio_master_callback_type]
        self._lib.VSTPluginMain.restype = POINTER(AEffect)
        self._effect = self._lib.VSTPluginMain(audio_master_callback_type(audio_master_callback)).contents

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
        # FIXME hard-coded 56
        self._dispatch(56, index=index, ptr=p)
        return p.contents

    @property
    def vst_version(self):
        # FIXME hard-coded
        return self._dispatch(58)

    @property
    def num_midi_in(self):
        # FIXME again
        return self._dispatch(60)

    @property
    def num_midi_out(self):
        # FIXME again
        return self._dispatch(61)

    def get_input_properties(self, index):
        ptr = pointer(VstPinProperties())
        # FIXME again
        is_supported = self._dispatch(33, index=index, ptr=ptr)
        print(is_supported)
        return 'abc'

    def get_output_properties(self, index):
        ptr = pointer(VstPinProperties())
        # FIXME again
        is_supported = self._dispatch(34, index=index, ptr=ptr)
        return ptr.contents

    #
    def __getattr__(self, attr):
        """We also try getattr(self._effect, attr) so we don't have to wrap all of those."""
        try:
            return getattr(self._effect, attr)
        except AttributeError:
            pass
        raise AttributeError('object VstPlugin has no attribute "{0}" and effect has no attribute "{0}'.format(attr))
