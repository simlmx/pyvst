import ctypes
from pyvst.midi import midi_data_as_bytes, midi_note_event, wrap_vst_events
from pyvst.vstwrap import VstMidiEvent


def test_note_on_bytes():
    assert midi_data_as_bytes(10, 10, 'note_on', 2) == b'\x91\x0A\x0A'
    assert midi_data_as_bytes(100, 100, 'note_off', 16) == b'\x8F\x64\x64'


def test_midi_note_event():
    midi_note_event(64, 100)
    # TODO test something


def test_wrap_vst_events():
    notes = [midi_note_event(64 + i, 100) for i in range(3)]
    wrapped = wrap_vst_events(notes)
    assert wrapped.num_events == 3
    events = wrapped.events
    note1 = events[0].contents
    assert note1.byte_size == ctypes.sizeof(VstMidiEvent)
    assert events[2].contents.byte_size == ctypes.sizeof(VstMidiEvent)

    note3 = events[2]
    note3 = ctypes.cast(note3, ctypes.POINTER(VstMidiEvent)).contents
