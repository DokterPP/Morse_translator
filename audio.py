import struct
import math
import re

class MorseCodeWav:
    def __init__(self, rate=44100, dot_duration=0.1, dash_duration=0.4, frequency=500.0):
        self.__rate = rate
        self.__dot_duration = dot_duration
        self.__dash_duration = dash_duration
        self.__frequency = frequency

        # Generate waveforms
        self.__dot_wave = self.__generate_wave(self.__dot_duration)
        self.__dash_wave = self.__generate_wave(self.__dash_duration)

        # Convert waveforms to bytes
        self.__byte_dot = self.__wave_to_bytes(self.__dot_wave)
        self.__byte_dash = self.__wave_to_bytes(self.__dash_wave)

        # Silence bytes
        self.__silence_short = self.__generate_silence(rate // 6) # 166ms silence
        self.__silence_long = self.__generate_silence(rate // 3)  # 333ms silence

    def __generate_wave(self, duration):
        num_samples = int(duration * self.__rate)
        wave = []
        for i in range(num_samples):
            t = i / self.__rate
            wave.append(math.sin(2 * math.pi * self.__frequency * t))
        return wave

    def __wave_to_bytes(self, wave):
        byte_wave = bytearray()
        for sample in wave:
            byte_wave.extend(struct.pack('<h', int(sample * 32767)))
        return byte_wave

    def __generate_silence(self, num_samples):
        return struct.pack('<h', 0) * num_samples

    def __append_wave(self, morse_sound, symbol):
        if symbol == '.':
            morse_sound.extend(self.__byte_dot)
            morse_sound.extend(self.__silence_short)
        elif symbol == '-':
            morse_sound.extend(self.__byte_dash)
            morse_sound.extend(self.__silence_short)
        elif symbol == ' ':
            morse_sound.extend(self.__silence_long)
        elif symbol == ',':
            morse_sound.extend(self.__silence_long)
        else:
            print(f"\nInvalid symbol: {symbol}")
            

    def __append_symbols(self, morse_sound, morse_code):
        if not morse_code:
            return
        self.__append_wave(morse_sound, morse_code[0])
        self.__append_symbols(morse_sound, morse_code[1:])

    def __write_wav_file(self, filename, morse_sound):
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
            f.write(struct.pack('<I', self.__rate))     # SampleRate
            f.write(struct.pack('<I', self.__rate * 2)) # ByteRate (SampleRate * NumChannels * BitsPerSample/8)
            f.write(struct.pack('<H', 2))             # BlockAlign (NumChannels * BitsPerSample/8)
            f.write(struct.pack('<H', 16))            # BitsPerSample

            # data subchunk
            f.write(b'data')
            f.write(struct.pack('<I', len(morse_sound))) # Subchunk2Size
            f.write(morse_sound)


    def convert_to_wav(self, morse_code, filename):
        for char in morse_code:
            if not re.match(r'[.\- \n,]', char.upper()):
                print(f"\nInvalid characters found in morse code. Please check the input file contents. Illegal characters found or wrong text file used. Use file checker to check for illegal characters.")
                input('\n'+"Press Enter, to continue....")
                return None
        morse_sound = bytearray()
        self.__append_symbols(morse_sound, morse_code)
        self.__write_wav_file(filename, morse_sound)
        input('\n'+"Press Enter, to continue....")
        
    
