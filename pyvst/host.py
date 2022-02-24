from ctypes import addressof, create_string_buffer
from warnings import warn

import numpy as np

from pyvst import VstPlugin
from pyvst.vstwrap import VstTimeInfoFlags, VstTimeInfo, AudioMasterOpcodes
from pyvst.midi import midi_note_event, wrap_vst_events


# Class inspired from MrsWatson's audioClock
class Transport:
    """
    Class responsible to know where we are in the "song".
    It knows the sample_rate and tempo and so it can convert the position in frames/seconds/beats.
    It also notes when it's changing from play/stop, etc, which can be asked by VSTs.
    """
    def __init__(self, sample_rate, tempo=120.):
        self._sample_rate = sample_rate
        self.tempo = tempo

        # position in frames
        self._position = 0.
        self.has_changed = False
        self.is_playing = False

    def step(self, num_frames):
        self._position += num_frames
        if not self.is_playing:
            self.is_playing = True
            self.has_changed = True
        else:
            self.has_changed = False

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            self.has_changed = True
        else:
            self.has_changed = False

    def reset(self):
        self.stop()
        self._position = 0.

    def get_position(self, unit='frame'):
        if unit == 'frame':
            return self._position
        elif unit == 'beat':  # same as a quarter
            return self.tempo * self._position / 60. / self._sample_rate
        elif unit == 'second':
            return self._position / self._sample_rate
        else:
            raise ValueError('Unknown unit "{}"'.format(unit))


class SimpleHost:
    """Simple host that holds a single (synth) vst."""

    _product_string = create_string_buffer(b'pyvst SimpleHost')

    def __init__(self, vst_filename=None, sample_rate=44100., tempo=120., block_size=512):
        self.sample_rate = sample_rate
        self.transport = Transport(sample_rate, tempo)
        self.block_size = block_size

        def callback(*args):
            return self._audio_master_callback(*args)

        self._callback = callback
        self._vst = None
        self._vst_path = None

        if vst_filename is not None:
            self.load_vst(vst_filename)

    @property
    def vst(self):
        if self._vst is None:
            raise RuntimeError('You must first load a vst using `self.load_vst`.')
        return self._vst

    def reload_vst(self):
        params = [self.vst.get_param_value(i) for i in range(self.vst.num_params)]
        self.vst.suspend()
        self.vst.close()
        del self._vst

        self.load_vst(self._path_to_so_file)
        for i, p in enumerate(params):
            self.vst.set_param_value(i, p)

    def load_vst(self, path_to_so_file):
        """
        Loads a vst. If there was already a vst loaded, we will release it.

        :param path_to_so_file: Path to the .so file to use as a plugin.
        """
        self._vst = VstPlugin(path_to_so_file, self._callback)

        # Not sure I need this but I've seen it in other hosts
        self.vst.open()

        if not self._vst.is_synth:
            raise RuntimeError('Your VST must be a synth!')

        self.vst.set_sample_rate(self.sample_rate)
        self.vst.set_block_size(self.block_size)
        self.vst.resume()

        # Warm up the VST by playing a quick note. It has fixed some issues for TyrellN6 where
        # otherwise the first note is funny.
        self._path_to_so_file = path_to_so_file
        self.play_note(note=64, min_duration=.1, max_duration=.1, note_duration=.1, velocity=127,
                       reload=False)

    def play_note(self, note=64, note_duration=.5, velocity=100, max_duration=5.,
                  min_duration=0.01, volume_threshold=0.000002, reload=False):
        """
        :param note_duration: Duration between the note on and note off midi events, in seconds.

        The audio will then last between `min_duration` and `max_duration`, stopping when
        sqrt(mean(signal ** 2)) falls under `volume_threshold` for a single buffer. For those
        arguments, `None` means they are ignored.

        :param reload: Will delete and reload the vst after having playing the note. It's an
            extreme way of making sure the internal state of the VST is reset. When False, we
            simply suspend() and resume() the VST (which should be enough in most cases).
        """
        if max_duration is not None and max_duration < note_duration:
            raise ValueError('max_duration ({}) is smaller than the midi note_duration ({})'
                             .format(max_duration, note_duration))

        if min_duration is not None and max_duration is not None and max_duration < min_duration:
            raise ValueError('max_duration ({}) is smaller than min_duration ({})'
                             .format(max_duration, min_duration))

        # Call this here to fail fast in case the VST has not been loaded
        self.vst

        # Convert the durations from seconds to frames
        min_duration = round(min_duration * self.sample_rate)
        max_duration = round(max_duration * self.sample_rate)

        note_on = midi_note_event(note, velocity)

        # nb of frames before the note_off events
        noteoff_is_in = round(note_duration * self.sample_rate)

        outputs = []

        self.transport.reset()

        # note_on is at time 0 anyway so we can do it before the loop
        self.vst.process_events(wrap_vst_events([note_on]))
        while True:
            if max_duration is not None and self.transport.get_position() > max_duration:
                break

            # If it's time for the note off
            if 0 <= noteoff_is_in < self.block_size:
                note_off = midi_note_event(note, 0, kind='note_off', delta_frames=noteoff_is_in)
                self.vst.process_events(wrap_vst_events([note_off]))

            output = self.vst.process(input=None, sample_frames=self.block_size)
            outputs.append(output)

            # If we are past the min_position, and if we have a volume_threshold, then we see if
            # we have enough volume to continue.
            if self.transport.get_position() > min_duration and volume_threshold:
                rms = np.sqrt((output ** 2).mean())
                if rms < volume_threshold:
                    break

            # We move transport in the future
            self.transport.step(self.block_size)
            # Which means the "noteoff is in" one block_size sooner
            noteoff_is_in -= self.block_size

        # Concatenate all the output buffers
        outputs = np.hstack(outputs)

        # Cut the extra of the last buffer if need be, to respect the `max_duration`.
        if max_duration is not None:
            outputs = outputs[:, :max_duration]

        # Reset the plugin to clear its state
        if reload:
            self.reload_vst()
        else:
            self.vst.suspend()
            self.vst.resume()

        return outputs

    def _audio_master_callback(self, effect, opcode, index, value, ptr, opt):
        # Note that there are a lot of missing opcodes here, I basically add them as I see VST
        # asking for them...
        if opcode == AudioMasterOpcodes.audioMasterVersion:
            return 2400
        # Deprecated but some VSTs still ask for it
        elif opcode == AudioMasterOpcodes.audioMasterWantMidi:
            return 1
        elif opcode == AudioMasterOpcodes.audioMasterGetTime:
            # Very much inspired from MrsWatson
            sample_pos = self.transport.get_position()
            sample_rate = self.sample_rate
            flags = 0

            # Always return those
            if self.transport.has_changed:
                flags |= VstTimeInfoFlags.kVstTransportChanged
            if self.transport.is_playing:
                flags |= VstTimeInfoFlags.kVstTransportPlaying

            if value & VstTimeInfoFlags.kVstNanosValid:
                warn('Asked for VstTimeInfoFlags.kVstNanosValid but not supported yet')

            # Depending on the passed mask, we'll returned what was asked
            mask = value
            if mask & VstTimeInfoFlags.kVstPpqPosValid:
                ppq_pos = self.transport.get_position(unit='beat')
                flags |= VstTimeInfoFlags.kVstPpqPosValid

            if mask & VstTimeInfoFlags.kVstTempoValid:
                tempo = self.transport.tempo
                flags |= VstTimeInfoFlags.kVstTempoValid

            # TODO: Should we warn that we don't support the other ones?

            # Make sure it doesn't get garbage collected
            self._last_time_info = VstTimeInfo(
                sample_pos=sample_pos,
                sample_rate=sample_rate,
                ppq_pos=ppq_pos,
                tempo=tempo,
                flags=flags,
            )
            return addressof(self._last_time_info)
        elif opcode == AudioMasterOpcodes.audioMasterGetProductString:
            return addressof(self._product_string)
        elif opcode == AudioMasterOpcodes.audioMasterIOChanged:
            return 0
        elif opcode == AudioMasterOpcodes.audioMasterGetCurrentProcessLevel:
            # This should mean "not supported by Host"
            return 0
        else:
            warn('Audio master call back opcode "{}" not supported yet'.format(opcode))
        return 0
