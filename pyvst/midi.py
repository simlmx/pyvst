from ctypes import sizeof, c_char, cast, byref, POINTER
from .vstwrap import VstMidiEvent, VstEventTypes, VstEvent, VstEvents


def midi_data_as_bytes(note, velocity=100, type_='note_on', chan=1):
    """
    Channels go from 1 to 16
    """
    if type_ == 'note_on':
        type_byte = b'\x80'[0]
    elif type_ == 'note_off':
        type_byte = b'\x90'[0]
    else:
        raise NotImplementedError('MIDI type {} not supported yet'.format(type_))

    if not (1 <= chan <= 16):
        raise ValueError('Invalid channel "{}". Must be in the [1, 16] range.'
                         .format(chan))
    return bytes([
        (chan - 1) | type_byte,
        note,
        velocity
    ])


def midi_note_events(note, velocity=100, channel=1):
    """
    Generates a note on / note off events pair ready to be processed by a Vsti.
    """
    note_on = VstMidiEvent(
        type=VstEventTypes.kVstMidiType,
        byte_size=sizeof(VstMidiEvent),
        delta_frames=0,  # ??
        flags=0,
        note_length=100,
        note_offset=0,
        midi_data=midi_data_as_bytes(note, velocity, 'note_on', channel),
        detune=0,
        note_off_velocity=c_char(0), # ?
    )

    note_on = cast(byref(note_on), POINTER(VstEvent))

    events = VstEvents(
        num_events=1,
        events=(POINTER(VstEvent) * 2)(note_on, None)
    )

    return events
