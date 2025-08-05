import pyaudio
import numpy as np
import wave
import threading
import warnings

class Recorder:
    '''
    The main Recorder class. Used to record and save speech. For simultaneous recordings, create multiple instances.

    Attributes:
        min_energy (int): The minimum amplitude of audio to be considered speech
        max_seconds_of_silence (int): The maximum seconds of silence before ending the recording (set to None to keep recording until .stop() is called)
        max_silence_multiplier (int): The maximum allowed multiplier of the previous amplitude for an outlier to qualify as silence
        standard_deviation_multiplier (int): The multiplier applied to the standard deviation of amplitude values, which is added to the mean to establish a safety margin when adjusting minimum energy for ambient noise.
    '''
    def __init__(self,  audio_path: str, format: int = pyaudio.paInt16, channels: int = 1, rate: int = 16000, frames_per_buffer: int = 1600, debug=False):
        '''
        Create an instance of the Recorder class.

        Args:
            audio_path (string): The file path to save audio in (must be of format .wav)
            format (int): The audio sample format
            channels (int): Number of channels used for input (1 for mono, 2 for stereo)
            rate (int): The sample rate of the audio in Hz
            frames_per_buffer: How many audio frames are read/written at a time
        
        Returns:
            None
        '''
        self.audio_path = audio_path
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.FRAMES_PER_BUFFER = frames_per_buffer
        self.debug = debug

        self.min_energy = 500
        self.max_seconds_of_silence = 1
        self.max_silence_multiplier = 2
        self.standard_deviation_multiplier = 1.5
        self.is_recording = False

        if (self.max_seconds_of_silence is not None):
            self._max_silent_buffers = (self.max_seconds_of_silence) / (self.FRAMES_PER_BUFFER / self.RATE)
        self._frames = []

        self.p = None
        self.stream = None
    
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def __del__(self):
        self.terminate()

    def _log(self, msg):
        if self.debug:
            print(msg)

    def record(self):
        '''
        Start or continue recording speech. Opens an audio stream if one is not already active.
        '''
        self.open()

        silent_buffers = 0
        self._frames = []

        try:
            self.is_recording = True
            self.stream.start_stream()
            while True:
                data = self.stream.read(self.FRAMES_PER_BUFFER)
                self._frames.append(data)

                audio_data = np.frombuffer(data, np.int16)
                amplitude = np.abs(audio_data).mean()

                self._log(f'amplitude: {amplitude:.2f}')

                if (self.max_seconds_of_silence is not None):
                    try:
                        last_amplitude = np.abs(np.frombuffer(self._frames[-2], np.int16)).mean()
                    except (IndexError, ValueError):
                        last_amplitude = self.min_energy
                    
                    self._log(f'last_amplitude: {last_amplitude:.2f}')
                
                    if (amplitude <= self.min_energy) or ((amplitude / (last_amplitude if last_amplitude != 0 else 1)) <= self.max_silence_multiplier and last_amplitude <= self.min_energy):
                        silent_buffers += 1
                    else:
                        silent_buffers = 0
                    
                    self._log(f'silent_buffers: {silent_buffers}')
                    
                    if silent_buffers >= self._max_silent_buffers:
                        break
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.save()
    
    def record_async(self, daemon=False):
        '''
        Calls the record method on a seperate thread. Used to prevent blocking the main thread when recording.

        Args:
            daemon (boolean): Whether or not the thread should be a daemon thread
        
        Returns:
            thread (Thread): The thread where the record method is being called
        '''
        thread = threading.Thread(target=self.record, daemon=daemon)
        thread.start()
        return thread
    
    def adjust_for_ambient_noise(self, adjustment_time: int = 1):
        '''
        Adjusts the minimum amplitude of audio to be considered speech based on the source's ambient noise.

        Args:
            adjustment_time (int): How many seconds to test for ambient noise 
        '''
        self.open()

        ambient_amplitudes = []

        self.stream.start_stream()

        # For adjustment_time seconds, add the amplitude of each buffer to the list
        while len(ambient_amplitudes) < (adjustment_time) / (self.FRAMES_PER_BUFFER / self.RATE):
            data = self.stream.read(self.FRAMES_PER_BUFFER)
            audio_data = np.frombuffer(data, np.int16)
            ambient_amplitudes.append(np.abs(audio_data).mean())

            self._log(f'ambient_amplitude: {np.abs(audio_data).mean():.2f}')

        # Calculate the average amplitude + standard deviation multiplied by a multiplier
        self.min_energy = np.mean(ambient_amplitudes) + (self.standard_deviation_multiplier * np.std(ambient_amplitudes))

        self._log(f'min_energy: {self.min_energy:.2f}')

        self.terminate()

    def stop(self):
        '''
        Stop recording speech and save audio.
        '''
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.is_recording = False
        if self.stream:
            self.stream.close()
        self.save()

    def pause(self):
        '''
        Pause recording speech. Does not save audio.
        '''
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.is_recording = False

    def save(self):
        '''
        Save currently recorded speech.
        '''
        audio = wave.open(self.audio_path, 'wb')
        audio.setnchannels(self.CHANNELS)
        audio.setsampwidth(self.p.get_sample_size(self.FORMAT))
        audio.setframerate(self.RATE)
        audio.writeframes(b''.join(self._frames))
        audio.close()
    
    def restart(self):
        '''
        Restarts what has been recorded.
        '''
        self._frames = []
    
    def open(self):
        '''
        Opens an audio stream.
        '''
        if self.stream:
            try:
                self.stream.close()
            except Exception as e:
                warnings.warn(f'Warning found while opening stream: {e}')
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
            start=False,
            input=True
        )
        
    def close(self):
        '''
        Closes the active stream.
        Does nothing if the stream has already been closed or no stream has been opened.
        '''
        if self.stream:
            try:
                self.stream.close()
                self.is_recording = False
            except Exception as e:
                self.is_recording = False
                warnings.warn(f'Warning found while closing stream: {e}')
    
    def terminate(self):
        '''
        Terminate the session and release system resources. You must call this method after all processes are complete to prevent resource leaks.
        Does nothing if no session has been created or has already been terminated.
        '''
        if (self.p):
            try:
                self.close()
                self.p.terminate()
                self.is_recording = False
            except Exception as e:
                self.is_recording = False
                warnings.warn(f'Warning found while terminating session: {e}')
            finally:
                self.stream = None
                self.p = None