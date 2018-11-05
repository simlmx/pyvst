import pytest

from pyvst import SimpleHost
from pyvst.host import Transport


def test_transport():
    transport = Transport(sample_rate=48000., tempo=120.)
    block_size = 512

    transport.step(block_size)
    assert transport.has_changed
    assert transport.is_playing

    transport.step(block_size)
    assert not transport.has_changed
    assert transport.is_playing
    assert transport.get_position() == block_size * 2

    transport.stop()
    assert transport.has_changed
    assert not transport.is_playing
    assert transport.get_position() == block_size * 2

    transport.reset()
    assert not transport.has_changed
    assert not transport.is_playing
    assert transport.get_position() == 0


def test_transport_get_position_units():
    sample_rate = 48000.
    tempo = 120.
    beat_per_sec = tempo / 60.
    block_size = 512
    transport = Transport(sample_rate=sample_rate, tempo=tempo)

    transport.step(block_size)
    transport.step(block_size)

    assert transport.get_position() == block_size * 2
    assert transport.get_position('frame') == block_size * 2
    assert transport.get_position('second') == block_size * 2 / sample_rate
    assert transport.get_position('beat') == beat_per_sec * (block_size * 2 / sample_rate)


def test_host_load_vst():
    host = SimpleHost()
    # TODO ship with some open source plugin
    with open('.test_plugin_path.txt') as f:
        path = f.read().strip()

    # It should raise if we try to access host.vst before we actually load it
    with pytest.raises(RuntimeError, match='You must first load'):
        host.vst

    # The first time we call `load_vst`, we need to pass a path!
    with pytest.raises(RuntimeError, match='The first time, you must'):
        host.load_vst()

    # Actually load it
    host.load_vst(path)
    # Second time it's fine without params, it will just reload it.
    host.load_vst()
    # Now it works
    host.vst


def test_play_note():
    host = SimpleHost()

    # TODO ship with some open source plugin
    with open('.test_plugin_path.txt') as f:
        path = f.read().strip()

    host.load_vst(path)

    # small max_duration compared to midi duration
    with pytest.raises(ValueError, match='is smaller than the midi note_duration'):
        host.play_note(64, note_duration=2., max_duration=1.)

    # smaller max_duration than min_duration
    with pytest.raises(ValueError, match='is smaller than min_duration'):
        host.play_note(64, note_duration=1., max_duration=1., min_duration=2.)

    # Try to play a note with a given duration
    output = host.play_note(note=76, velocity=127, note_duration=.2, max_duration=3., min_duration=3.)
    assert output.shape == (2, 44100 * 3)
    # Make sure there was some noise!
    assert output.max() > .1

    # Automatic stopping of the sound
    output = host.play_note(64, note_duration=0.1, max_duration=60.)
    assert 44100 * 0.1 < output.shape[1] < 44100 * 58
