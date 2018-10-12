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


def test_host():
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

    # Try to play a note
    output = host.play_note(note=76, velocity=127, duration=.2, total_duration=3.)
    # Make sure there was some noise!
    assert output.max() > .1
