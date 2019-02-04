import random

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


def test_play_note(host):

    # small max_duration compared to midi duration
    with pytest.raises(ValueError, match='is smaller than the midi note_duration'):
        host.play_note(64, note_duration=2., max_duration=1.)

    # smaller max_duration than min_duration
    with pytest.raises(ValueError, match='is smaller than min_duration'):
        host.play_note(64, note_duration=1., max_duration=1., min_duration=2.)

    # Try to play a note with a given duration
    output = host.play_note(note=76, velocity=127, note_duration=.2, max_duration=3.,
                            min_duration=3.)
    assert output.shape == (2, 44100 * 3)
    # Make sure there was some noise!
    assert output.max() > .1

    # Automatic stopping of the sound
    output = host.play_note(64, note_duration=0.1, max_duration=60.)
    assert 44100 * 0.1 < output.shape[1] < 44100 * 58


def test_play_note_twice(host):
    vel = 127
    sound1 = host.play_note(note=64, min_duration=1., max_duration=2., note_duration=1.,
                            velocity=vel)
    sound2 = host.play_note(note=65, min_duration=1., max_duration=2., note_duration=1.,
                            velocity=vel)
    # import numpy as np
    # np.save('patate1.npy', sound1)
    # np.save('patate2.npy', sound2)
    # TODO compare with something more resistant to noise
    # assert abs(sound1 - sound2).mean() / abs(sound1).mean() < 0.001

    # after changing all the parameters, it should still work
    for i in range(host.vst.num_params):
        host.vst.set_param_value(i, random.random())

    # TODO same
    sound1 = host.play_note()
    sound2 = host.play_note()


# FIXME: For the same reason as above, this is unreliable
# def test_play_note_changing_params(host):
#     sound1 = host.play_note()

#     for i in range(host.vst.num_params):
#         host.vst.set_param_value(i, random.random())

#     sound2 = host.play_note()

#     for i in range(host.vst.num_params):
#         host.vst.set_param_value(i, random.random())

#     sound3 = host.play_note()

#     assert sound1.shape != sound2.shape or abs(sound1 - sound2).mean() / abs(sound1).mean() > 0.0001
#     assert sound2.shape != sound3.shape or abs(sound2 - sound3).mean() / abs(sound2).mean()  > 0.0001
