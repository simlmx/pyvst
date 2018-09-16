from pyvst.midi import midi_data_as_bytes


def test_note_on_bytes():
    assert midi_data_as_bytes(10, 10, 'note_on', 2) == b'\x81\x0A\x0A'
    assert midi_data_as_bytes(100, 100, 'note_off', 16) == b'\x9F\x64\x64'
