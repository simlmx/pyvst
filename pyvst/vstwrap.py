from ctypes import (cdll, Structure, POINTER, CFUNCTYPE,
                    c_void_p, c_int, c_float, c_int32, c_double, c_char,
                    addressof, byref, pointer)
from enum import IntEnum


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

    # [ptr]: #VstEvents*  @see AudioEffectX::processEvents
    effProcessEvents = 25

    # [index]: parameter index [return value]: 1=true, 0=false  @see AudioEffectX::canParameterBeAutomated
    effCanBeAutomated = 26
    # [index]: parameter index [ptr]: parameter string [return value]: true for success  @see AudioEffectX::string2parameter
    effString2Parameter = 27

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetNumProgramCategories)

    # [index]: program index [ptr]: buffer for program name, limited to #kVstMaxProgNameLen [return value]: true for success  @see AudioEffectX::getProgramNameIndexed
    effGetProgramNameIndexed = 29

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effCopyProgram)
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effConnectInput)
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effConnectOutput)

    # [index]: input index [ptr]: #VstPinProperties* [return value]: 1 if supported  @see AudioEffectX::getInputProperties
    effGetInputProperties = 33
    # [index]: output index [ptr]: #VstPinProperties* [return value]: 1 if supported  @see AudioEffectX::getOutputProperties
    effGetOutputProperties = 34
    # [return value]: category  @see VstPlugCategory @see AudioEffectX::getPlugCategory
    effGetPlugCategory = 35

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetCurrentPosition)
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetDestinationBuffer)

    # [ptr]: #VstAudioFile array [value]: count [index]: start flag  @see AudioEffectX::offlineNotify
    effOfflineNotify = 38
    # [ptr]: #VstOfflineTask array [value]: count  @see AudioEffectX::offlinePrepare
    effOfflinePrepare = 39
    # [ptr]: #VstOfflineTask array [value]: count  @see AudioEffectX::offlineRun
    effOfflineRun = 40

    # [ptr]: #VstVariableIo*  @see AudioEffectX::processVariableIo
    effProcessVarIo = 41
    # [value]: input #VstSpeakerArrangement* [ptr]: output #VstSpeakerArrangement*  @see AudioEffectX::setSpeakerArrangement
    effSetSpeakerArrangement = 42

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effSetBlockSizeAndSampleRate)

    # [value]: 1 = bypass, 0 = no bypass  @see AudioEffectX::setBypass
    effSetBypass = 44
    # [ptr]: buffer for effect name limited to #kVstMaxEffectNameLen  @see AudioEffectX::getEffectName
    effGetEffectName = 45

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetErrorText)

    # [ptr]: buffer for effect vendor string, limited to #kVstMaxVendorStrLen  @see AudioEffectX::getVendorString
    effGetVendorString = 47
    # [ptr]: buffer for effect vendor string, limited to #kVstMaxProductStrLen  @see AudioEffectX::getProductString
    effGetProductString = 48
    # [return value]: vendor-specific version  @see AudioEffectX::getVendorVersion
    effGetVendorVersion = 49
    # no definition, vendor specific handling  @see AudioEffectX::vendorSpecific
    effVendorSpecific = 50
    # [ptr]: "can do" string [return value]: 0: "don't know" -1: "no" 1: "yes"  @see AudioEffectX::canDo
    effCanDo = 51
    # [return value]: tail size (for example the reverb time of a reverb plug-in); 0 is default (return 1 for 'no tail')
    effGetTailSize = 52

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effIdle)
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetIcon)
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effSetViewPosition)

    # [index]: parameter index [ptr]: #VstParameterProperties* [return value]: 1 if supported  @see AudioEffectX::getParameterProperties
    effGetParameterProperties = 56

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effKeysRequired)

    # [return value]: VST version  @see AudioEffectX::getVstVersion
    effGetVstVersion = 58

    # [value]: @see VstProcessPrecision  @see AudioEffectX::setProcessPrecision
    effSetProcessPrecision = 59
    # [return value]: number of used MIDI input channels (1-15)  @see AudioEffectX::getNumMidiInputChannels
    effGetNumMidiInputChannels = 60
    # [return value]: number of used MIDI output channels (1-15)  @see AudioEffectX::getNumMidiOutputChannels
    effGetNumMidiOutputChannels = 61


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


AUDIO_MASTER_CALLBACK_TYPE = CFUNCTYPE(c_void_p, POINTER(AEffect), c_int32, c_int32, c_int, c_void_p, c_float)
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
        # FIXME not finished
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
