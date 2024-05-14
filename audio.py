import struct
import math

class MorseCodeWav:
    def __init__(self, rate=44100, dot_duration=0.1, dash_duration=0.4, frequency=500.0):
        self.rate = rate
        self.dot_duration = dot_duration
        self.dash_duration = dash_duration
        self.frequency = frequency

        # Generate waveforms
        self._dot_wave = self._generate_wave(self.dot_duration)
        self._dash_wave = self._generate_wave(self.dash_duration)

        # Convert waveforms to bytes
        self._byte_dot = self._wave_to_bytes(self._dot_wave)
        self._byte_dash = self._wave_to_bytes(self._dash_wave)

        # Silence bytes
        self._silence_short = self._generate_silence(rate // 6) # 166ms silence
        self._silence_long = self._generate_silence(rate // 3)  # 333ms silence

    def _generate_wave(self, duration):
        num_samples = int(duration * self.rate)
        wave = []
        for i in range(num_samples):
            t = i / self.rate
            wave.append(math.sin(2 * math.pi * self.frequency * t))
        return wave

    def _wave_to_bytes(self, wave):
        byte_wave = bytearray()
        for sample in wave:
            byte_wave.extend(struct.pack('<h', int(sample * 32767)))
        return byte_wave

    def _generate_silence(self, num_samples):
        return struct.pack('<h', 0) * num_samples

    def _append_wave(self, morse_sound, symbol):
        if symbol == '.':
            morse_sound.extend(self._byte_dot)
            morse_sound.extend(self._silence_short)
        elif symbol == '-':
            morse_sound.extend(self._byte_dash)
            morse_sound.extend(self._silence_short)
        elif symbol == ' ':
            morse_sound.extend(self._silence_long)
        elif symbol == ',':
            morse_sound.extend(self._silence_long)
        else:
            print(f"\nInvalid symbol: {symbol}")
            

    def _append_symbols(self, morse_sound, morse_code):
        if not morse_code:
            return
        self._append_wave(morse_sound, morse_code[0])
        self._append_symbols(morse_sound, morse_code[1:])

    def _write_wav_file(self, filename, morse_sound):
        with open(filename, 'wb') as f:
            # RIFF header
            f.write(b'RIFF')
            f.write(struct.pack('<I', 36 + len(morse_sound))) # Chunk size
            f.write(b'WAVE')

            # fmt subchunk
            f.write(b'fmt ')
            f.write(struct.pack('<I', 16))            # Subchunk1Size (16 for PCM)
            f.write(struct.pack('<H', 1))             # AudioFormat (1 for PCM)
            f.write(struct.pack('<H', 1))             # NumChannels
            f.write(struct.pack('<I', self.rate))     # SampleRate
            f.write(struct.pack('<I', self.rate * 2)) # ByteRate (SampleRate * NumChannels * BitsPerSample/8)
            f.write(struct.pack('<H', 2))             # BlockAlign (NumChannels * BitsPerSample/8)
            f.write(struct.pack('<H', 16))            # BitsPerSample

            # data subchunk
            f.write(b'data')
            f.write(struct.pack('<I', len(morse_sound))) # Subchunk2Size
            f.write(morse_sound)


    def convert_to_wav(self, morse_code, filename):
        morse_sound = bytearray()
        self._append_symbols(morse_sound, morse_code)
        self._write_wav_file(filename, morse_sound)
        input('\n'+"Press Enter, to continue....")
