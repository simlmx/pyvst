from ctypes import (Structure, POINTER, CFUNCTYPE, c_void_p, c_float,
                    c_int32, c_double, c_char, c_int16, c_int64)
from enum import IntEnum


# Corresponds to VstIntPtr in aeffect.h
# We're assuming we are working in 64bit
vst_int_ptr = c_int64


class AudioMasterOpcodes(IntEnum):
    # [index]: parameter index [opt]: parameter value  @see AudioEffect::setParameterAutomated
    audioMasterAutomate = 0
    # [return value]: Host VST version (for example 2400 for VST 2.4) @see AudioEffect::getMasterVersion
    audioMasterVersion = 1
    # [return value]: current unique identifier on shell plug-in  @see AudioEffect::getCurrentUniqueId
    audioMasterCurrentId = 2
    # no arguments  @see AudioEffect::masterIdle
    audioMasterIdle = 3

    # \deprecated deprecated in VST 2.4 r2
    # DECLARE_VST_DEPRECATED (audioMasterPinConnected)
    # \deprecated deprecated in VST 2.4
    audioMasterWantMidi = 6

    # [return value]: #VstTimeInfo* or null if not supported [value]: request mask  @see VstTimeInfoFlags @see AudioEffectX::getTimeInfo
    audioMasterGetTime = 7
    # [ptr]: pointer to #VstEvents  @see VstEvents @see AudioEffectX::sendVstEventsToHost
    audioMasterProcessEvents = 8

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetTime),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterTempoAt),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetNumAutomatableParameters),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetParameterQuantization),

    # [return value]: 1 if supported  @see AudioEffectX::ioChanged
    audioMasterIOChanged = 13

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterNeedIdle),

    # [index]: new width [value]: new height [return value]: 1 if supported  @see AudioEffectX::sizeWindow
    audioMasterSizeWindow = 15
    # [return value]: current sample rate  @see AudioEffectX::updateSampleRate
    audioMasterGetSampleRate = 16
    # [return value]: current block size  @see AudioEffectX::updateBlockSize
    audioMasterGetBlockSize = 17
    # [return value]: input latency in audio samples  @see AudioEffectX::getInputLatency
    audioMasterGetInputLatency = 18
    # [return value]: output latency in audio samples  @see AudioEffectX::getOutputLatency
    audioMasterGetOutputLatency = 19

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetPreviousPlug),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetNextPlug),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterWillReplaceOrAccumulate),

    # [return value]: current process level  @see VstProcessLevels
    audioMasterGetCurrentProcessLevel = 23
    # [return value]: current automation state  @see VstAutomationStates
    audioMasterGetAutomationState = 24

    # [index]: numNewAudioFiles [value]: numAudioFiles [ptr]: #VstAudioFile*  @see AudioEffectX::offlineStart
    audioMasterOfflineStart = 25
    # [index]: bool readSource [value]: #VstOfflineOption* @see VstOfflineOption [ptr]: #VstOfflineTask*  @see VstOfflineTask @see AudioEffectX::offlineRead
    audioMasterOfflineRead = 26
    # @see audioMasterOfflineRead @see AudioEffectX::offlineRead
    audioMasterOfflineWrite = 27
    # @see AudioEffectX::offlineGetCurrentPass
    audioMasterOfflineGetCurrentPass = 28
    # @see AudioEffectX::offlineGetCurrentMetaPass
    audioMasterOfflineGetCurrentMetaPass = 29

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetOutputSampleRate),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetOutputSpeakerArrangement),

    # [ptr]: char buffer for vendor string, limited to #kVstMaxVendorStrLen  @see AudioEffectX::getHostVendorString
    audioMasterGetVendorString = 32
    # [ptr]: char buffer for vendor string, limited to #kVstMaxProductStrLen  @see AudioEffectX::getHostProductString
    audioMasterGetProductString = 33
    # [return value]: vendor-specific version  @see AudioEffectX::getHostVendorVersion
    audioMasterGetVendorVersion = 34
    # no definition, vendor specific handling  @see AudioEffectX::hostVendorSpecific
    audioMasterVendorSpecific = 35

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetIcon),

    # [ptr]: "can do" string [return value]: 1 for supported
    audioMasterCanDo= 37
    # [return value]: language code  @see VstHostLanguage
    audioMasterGetLanguage = 38

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterOpenWindow),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterCloseWindow),

    # [return value]: FSSpec on MAC, else char*  @see AudioEffectX::getDirectory
    audioMasterGetDirectory = 41
    # no arguments
    audioMasterUpdateDisplay = 42
    # [index]: parameter index  @see AudioEffectX::beginEdit
    audioMasterBeginEdit = 43
    # [index]: parameter index  @see AudioEffectX::endEdit
    audioMasterEndEdit = 44
    # [ptr]: VstFileSelect* [return value]: 1 if supported  @see AudioEffectX::openFileSelector
    audioMasterOpenFileSelector = 45
    # [ptr]: VstFileSelect*  @see AudioEffectX::closeFileSelector
    audioMasterCloseFileSelector = 46

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterEditFile),

    # \deprecated deprecated in VST 2.4 [ptr]: char[2048] or sizeof (FSSpec) [return value]: 1 if supported  @see AudioEffectX::getChunkFile
    # DECLARE_VST_DEPRECATED (audioMasterGetChunkFile),

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetInputSpeakerArrangement)


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
    kVstMaxProgNameLen = 24
    # used for #effGetParamLabel, #effGetParamDisplay, #effGetParamName
    kVstMaxParamStrLen = 8
    # used for #effGetVendorString, #audioMasterGetVendorString
    kVstMaxVendorStrLen = 64
    # used for #effGetProductString, #audioMasterGetProductString
    kVstMaxProductStrLen = 64
    # used for #effGetEffectName
    kVstMaxEffectNameLen = 32


class Vst2StringConstants:
    # used for #MidiProgramName, #MidiProgramCategory, #MidiKeyName, #VstSpeakerProperties, #VstPinProperties
    kVstMaxNameLen = 64
    # used for #VstParameterProperties->label, #VstPinProperties->label
    kVstMaxLabelLen = 64
    # used for #VstParameterProperties->shortLabel, #VstPinProperties->shortLabel
    kVstMaxShortLabelLen = 8
    # used for #VstParameterProperties->label
    kVstMaxCategLabelLen = 24
    # used for #VstAudioFile->name
    kVstMaxFileNameLen = 100


class AEffect(Structure):
    pass


# typedef	VstIntPtr (VSTCALLBACK *audioMasterCallback) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
AUDIO_MASTER_CALLBACK_TYPE = CFUNCTYPE(vst_int_ptr, POINTER(AEffect), c_int32, c_int32, vst_int_ptr, c_void_p, c_float)
# typedef VstIntPtr (VSTCALLBACK *AEffectDispatcherProc) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
_AEFFECT_DISPATCHER_PROC_TYPE = CFUNCTYPE(vst_int_ptr, POINTER(AEffect), c_int32, c_int32, vst_int_ptr, c_void_p, c_float)
# typedef void (VSTCALLBACK *AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sampleFrames);
# _AEFFECT_PROCESS_PROC_TYPE = CFUNCTYPE(c_void_p,
#                                       POINTER(AEffect),
#                                       POINTER(POINTER(c_float)),
#                                       POINTER(POINTER(c_float)),
#                                       c_int32,)
_GET_PARAMETER_TYPE = CFUNCTYPE(c_float, POINTER(AEffect), c_int32)
_SET_PARAMETER_TYPE = CFUNCTYPE(None, POINTER(AEffect), c_int32, c_float)
# typedef void (VSTCALLBACK *AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sampleFrames);
_AEFFECT_PROCESS_PROC = CFUNCTYPE(None, POINTER(AEffect), POINTER(POINTER(c_float)), POINTER(POINTER(c_float)), c_int32)
# typedef void (VSTCALLBACK *AEffectProcessDoubleProc) (AEffect* effect, double** inputs, double** outputs, VstInt32 sampleFrames);
_AEFFECT_PROCESS_DOUBLE_PROC = CFUNCTYPE(None, POINTER(AEffect), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), c_int32)


AEffect._fields_ = [
    ('magic', c_int32),
    ('dispatcher', _AEFFECT_DISPATCHER_PROC_TYPE),
    ('_process', c_void_p),
    ('set_parameter', _SET_PARAMETER_TYPE),
    ('get_parameter', _GET_PARAMETER_TYPE),
    ('num_programs', c_int32),
    ('num_params', c_int32),
    ('num_inputs', c_int32),
    ('num_outputs', c_int32),
    ('flags', c_int32),
    ('resvd1', vst_int_ptr),
    ('resvd2', vst_int_ptr),
    ('initial_delay', c_int32),
    ('_realQualities', c_int32),
    ('_offQualities', c_int32),
    ('_ioRatio', c_float),
    ('object', c_void_p),
    ('user', c_void_p),
    ('unique_id', c_int32),
    ('version', c_int32),
    ('process_replacing', _AEFFECT_PROCESS_PROC),
    ('process_double_replacing', _AEFFECT_PROCESS_DOUBLE_PROC),
    ('_future1', c_char * 56),
]


class VstParameterProperties(Structure):
    _fields_ = [
        ('step_float', c_float),
        ('small_step_float', c_float),
        ('large_step_float', c_float),
        ('label', c_char * Vst2StringConstants.kVstMaxLabelLen),
        ('flags', c_int32),
        ('min_int', c_int32),
        ('max_int', c_int32),
        ('step_int', c_int32),
        ('large_step_int', c_int32),
        ('short_label', c_char * Vst2StringConstants.kVstMaxShortLabelLen),
        ('display_index', c_int16),
        ('category', c_int16),
        ('num_params_in_category', c_int16),
        ('reserved', c_int16),
        ('category_label', c_char * Vst2StringConstants.kVstMaxCategLabelLen),
        ('future', c_char * 16),
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
        ('future', c_char * 48),
    ]


# Note: In python3.6 we could use `IntFlag`.
class VstParameterFlags(IntEnum):
    # parameter is a switch (on/off)
    kVstParameterIsSwitch = 1 << 0
    # minInteger, maxInteger valid
    kVstParameterUsesIntegerMinMax = 1 << 1
    # stepFloat, smallStepFloat, largeStepFloat valid
    kVstParameterUsesFloatStep = 1 << 2
    # stepInteger, largeStepInteger valid
    kVstParameterUsesIntStep = 1 << 3
    # displayIndex valid
    kVstParameterSupportsDisplayIndex = 1 << 4
    # category, etc. valid
    kVstParameterSupportsDisplayCategory = 1 << 5
    #  set if parameter value can ramp up/down
    kVstParameterCanRamp = 1 << 6


class VstAEffectFlags(IntEnum):
    # set if the plug-in provides a custom editor
    effFlagsHasEditor = 1 << 0
    # supports replacing process mode (which should the default mode in VST 2.4)
    effFlagsCanReplacing = 1 << 4
    # program data is handled in formatless chunks
    effFlagsProgramChunks = 1 << 5
    # plug-in is a synth (VSTi), Host may assign mixer channels for its outputs
    effFlagsIsSynth = 1 << 8
    # plug-in does not produce sound when input is all silence
    effFlagsNoSoundInStop = 1 << 9

    # plug-in supports double precision processing
    effFlagsCanDoubleReplacing = 1 << 12

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsHasClip) = 1 << 1,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsHasVu)   = 1 << 2,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsCanMono) = 1 << 3,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsExtIsAsync)   = 1 << 10,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsExtHasBuffer) = 1 << 11


class VstEvent(Structure):
    _fields_ = [
        # @see VstEventTypes
        ('type', c_int32),
        # size of this event, excl. type and byteSize
        ('byte_size', c_int32),
        # sample frames related to the current block start sample position
        ('delta_frames', c_int32),
        # generic flags, none defined yet
        ('flags', c_int32),
        # data size may vary, depending on event type
        ('data', c_char * 16),
    ]


class VstEventTypes(IntEnum):
    # MIDI event  @see VstMidiEvent
    kVstMidiType = 1
    # \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstAudioType),
    # \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstVideoType),
    # \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstParameterType),
    # \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstTriggerType),
    # MIDI system exclusive  @see VstMidiSysexEvent
    kVstSysExType = 6


class VstEvents(Structure):
    _fields_ = [
        # number of Events in array
        ('num_events', c_int32),
        # zero (Reserved for future use)
        ('reserved', vst_int_ptr),
        # event pointer array, variable size
        ('events', POINTER(VstEvent) * 2),
    ]

def get_vst_events_struct(num_events):
    """Class factory to get a VstEvents class with the right length for the "events" field."""
    class VstEventsN(Structure):
        _fields_ = [
            # number of Events in array
            ('num_events', c_int32),
            # zero (Reserved for future use)
            ('reserved', vst_int_ptr),
            # event pointer array, variable size
            ('events', POINTER(VstEvent) * num_events),
        ]
    return VstEventsN


class VstMidiEvent(Structure):
    _fields_ = [
        # kVstMidiType
        ('type', c_int32),
        # sizeof (VstMidiEvent)
        ('byte_size', c_int32),
        # sample frames related to the current block start sample position
        ('delta_frames', c_int32),
        # @see VstMidiEventFlags
        ('flags', c_int32),
        # (in sample frames) of entire note, if available, else 0
        ('note_length', c_int32),
        # offset (in sample frames) into note from note start if available, else 0
        ('note_offset', c_int32),
        # 1 to 3 MIDI bytes; midiData[3] is reserved (zero)
        ('midi_data', c_char * 4),
        # -64 to +63 cents; for scales other than 'well-tempered' ('microtuning')
        ('detune', c_char),
        # Note Off Velocity [0, 127]
        ('note_off_velocity', c_char),
        # zero (Reserved for future use)
        ('reserved1', c_char),
        # zero (Reserved for future use)
        ('reserved2', c_char),
    ]


# Note: In python3.6 we could use `IntFlag`.
class VstMidiEventFlags(IntEnum):
    #  means that this event is played life (not in playback from a sequencer track).
    # This allows the Plug-In to handle these flagged events with higher priority, especially when
    # the Plug-In has a big latency (AEffect::initialDelay)
    kVstMidiEventIsRealtime = 1 << 0


class VstTimeInfo(Structure):
    __fields__ = [
        # current Position in audio samples (always valid)
        ('sample_pos', c_double),
        # current Sample Rate in Herz (always valid)
        ('sample_rate', c_double),
        # System Time in nanoseconds (10^-9 second)
        ('nano_seconds', c_double),
        # Musical Position, in Quarter Note (1.0 equals 1 Quarter Note)
        ('ppq_pos', c_double),
        # current Tempo in BPM (Beats Per Minute)
        ('tempo', c_double),
        # last Bar Start Position, in Quarter Note
        ('bar_start_pos', c_double),
        # Cycle Start (left locator), in Quarter Note
        ('cycle_start_pos', c_double),
        # Cycle End (right locator), in Quarter Note
        ('cycle_end_pos', c_double),
        # Time Signature Numerator (e.g. 3 for 3/4)
        ('time_sig_numerator', c_int32),
        # Time Signature Denominator (e.g. 4 for 3/4)
        ('time_sig_denominator', c_int32),
        # SMPTE offset (in SMPTE subframes (bits; 1/80 of a frame)). The current SMPTE position can be calculated using #samplePos, #sampleRate, and #smpteFrameRate.
        ('smpte_offset', c_int32),
        # @see VstSmpteFrameRate
        ('smpte_frame_rate', c_int32),
        # MIDI Clock Resolution (24 Per Quarter Note), can be negative (nearest clock)
        ('samples_to_next_clock', c_int32),
        # @see VstTimeInfoFlags
        ('flags', c_int32),
    ]

class VstTimeInfoFlags(IntEnum):
    # indicates that play, cycle or record state has changed
    kVstTransportChanged = 1
    # set if Host sequencer is currently playing
    kVstTransportPlaying = 1 << 1
    # set if Host sequencer is in cycle mode
    kVstTransportCycleActive = 1 << 2
    # set if Host sequencer is in record mode
    kVstTransportRecording = 1 << 3
    # set if automation write mode active (record parameter changes)
    kVstAutomationWriting = 1 << 6
    # set if automation read mode active (play parameter changes)
    kVstAutomationReading = 1 << 7
    # VstTimeInfo::nanoSeconds valid
    kVstNanosValid = 1 << 8
    # VstTimeInfo::ppqPos valid
    kVstPpqPosValid = 1 << 9
    # VstTimeInfo::tempo valid
    kVstTempoValid = 1 << 10
    # VstTimeInfo::barStartPos valid
    kVstBarsValid = 1 << 11
    # VstTimeInfo::cycleStartPos and VstTimeInfo::cycleEndPos valid
    kVstCyclePosValid = 1 << 12
    # VstTimeInfo::timeSigNumerator and VstTimeInfo::timeSigDenominator valid
    kVstTimeSigValid = 1 << 13
    # VstTimeInfo::smpteOffset and VstTimeInfo::smpteFrameRate valid
    kVstSmpteValid = 1 << 14
    # VstTimeInfo::samplesToNextClock valid
    kVstClockValid = 1 << 15


class VstAudioFileFlags(IntEnum):
    # set by Host (in call #offlineNotify)
    kVstOfflineReadOnly = 1 << 0
    # set by Host (in call #offlineNotify)
    kVstOfflineNoRateConversion = 1 << 1
    # set by Host (in call #offlineNotify)
    kVstOfflineNoChannelChange = 1 << 2
    # set by plug-in (in call #offlineStart)
    kVstOfflineCanProcessSelection = 1 << 10
    # set by plug-in (in call #offlineStart)
    kVstOfflineNoCrossfade = 1 << 11
    # set by plug-in (in call #offlineStart)
    kVstOfflineWantRead = 1 << 12
    # set by plug-in (in call #offlineStart)
    kVstOfflineWantWrite = 1 << 13
    # set by plug-in (in call #offlineStart)
    kVstOfflineWantWriteMarker = 1 << 14
    # set by plug-in (in call #offlineStart)
    kVstOfflineWantMoveCursor = 1 << 15
    # set by plug-in (in call #offlineStart)
    kVstOfflineWantSelect = 1 << 16


class VstPlugCategory(IntEnum):
    # Unknown, category not implemented
    kPlugCategUnknown = 0
    # Simple Effect
    kPlugCategEffect = 1
    # VST Instrument (Synths, samplers,...)
    kPlugCategSynth = 2
    # Scope, Tuner, ...
    kPlugCategAnalysis = 3
    # Dynamics, ...
    kPlugCategMastering = 4
    # Panners, ...
    kPlugCategSpacializer = 5
    # Delays and Reverbs
    kPlugCategRoomFx = 6
    # Dedicated surround processor
    kPlugSurroundFx = 7
    # Denoiser, ...
    kPlugCategRestoration = 8
    # Offline Process
    kPlugCategOfflineProcess = 9
    # Plug-in is container of other plug-ins  @see effShellGetNextPlugin
    kPlugCategShell = 10
    # ToneGenerator, ...
    kPlugCategGenerator = 11
    # Marker to count the categories
    kPlugCategMaxCount = 12
