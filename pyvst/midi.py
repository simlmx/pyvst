from ctypes import sizeof, cast, POINTER, pointer
from .vstwrap import VstMidiEvent, VstEventTypes, VstEvent, get_vst_events_struct


def _check_channel_valid(channel):
    if not (1 <= channel <= 16):
        raise ValueError('Invalid channel "{}". Must be in the [1, 16] range.'
                         .format(channel))


def midi_note_as_bytes(note, velocity=100, kind='note_on', channel=1):
    """
    :param channel: Midi channel (those are 1-indexed)
    """
    if kind == 'note_on':
        kind_byte = b'\x90'[0]
    elif kind == 'note_off':
        kind_byte = b'\x80'[0]
    else:
        raise NotImplementedError('MIDI type {} not supported yet'.format(kind))

    _check_channel_valid(channel)

    return bytes([
        (channel - 1) | kind_byte,
        note,
        velocity
    ])


def midi_note_event(note, velocity=100, channel=1, kind='note_on', delta_frames=0):
    """
    Generates a note (on or off) midi event (VstMidiEvent).

    :param note: midi note number
    :param velocity: 0-127
    :param channel: 1-16
    :param kind: "note_on" or "note_off"
    :delta_frames: In how many frames should the event happen.
    """
    note_on = VstMidiEvent(
        type=VstEventTypes.kVstMidiType,
        byte_size=sizeof(VstMidiEvent),
        delta_frames=delta_frames,
        flags=0,
        note_length=0,
        note_offset=0,
        midi_data=midi_note_as_bytes(note, velocity, kind, channel),
        detune=0,
        note_off_velocity=127,
    )
    return note_on


def wrap_vst_events(midi_events):
    """Wraps a list VstMidiEvent into a VstEvents structure."""
    p_midi_events = [pointer(x) for x in midi_events]
    p_midi_events = [cast(x, POINTER(VstEvent)) for x in p_midi_events]
    p_array = (POINTER(VstEvent) * len(midi_events))
    Struct = get_vst_events_struct(len(midi_events))
    events = Struct(
        num_events=len(midi_events),
        events=p_array(*p_midi_events)
    )
    return events


def all_sounds_off_event(channel=1):

    _check_channel_valid(channel)

    # See https://www.midi.org/specifications-old/item/table-1-summary-of-midi-message
    midi_data = bytes([
        (channel - 1) | b'\xb0'[0],
        120,
        0,
    ])

    midi_event = VstMidiEvent(
        type=VstEventTypes.kVstMidiType,
        byte_size=sizeof(VstMidiEvent),
        delta_frames=0,
        flags=0,
        note_length=0,
        note_offset=0,
        midi_data=midi_data,
        detune=0,
        note_off_velocity=0,
    )

    return midi_event
