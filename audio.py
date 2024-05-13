import numpy as np
import wavio

# Parameters
rate = 44100    # samples per second
T_dot = 0.1     # dot duration (seconds)
T_dash = 0.4    # dash duration (seconds)
f = 500.0       # sound frequency (Hz)

# Compute waveform samples for dot and dash
t_dot = np.linspace(0, T_dot, int(T_dot*rate), endpoint=False)
t_dash = np.linspace(0, T_dash, int(T_dash*rate), endpoint=False)
dot = np.sin(2*np.pi * f * t_dot)
dash = np.sin(2*np.pi * f * t_dash)

def write_morse_code_to_wav(morse_code, filename):
    morse_sound = np.array([])
    for symbol in morse_code:
        if symbol == '.':
            morse_sound = np.append(morse_sound, dot)
            morse_sound = np.append(morse_sound, np.zeros(rate//6))  # 166ms silence
        elif symbol == '-':
            morse_sound = np.append(morse_sound, dash)
            morse_sound = np.append(morse_sound, np.zeros(rate//6))  # 166ms silence
            
        elif symbol == ' ':
            morse_sound = np.append(morse_sound, np.zeros(rate//3))  # 333ms silence
            
        elif symbol == ',':
            morse_sound = np.append(morse_sound, np.zeros(rate//100))   # 10ms silence
            
    wavio.write(filename, morse_sound, rate, sampwidth=3)

# Test the function
write_morse_code_to_wav('....,.,.-..,.-..,---, ,-,....,..,..., ,..,..., ,.-, ,-,.-.,.-,-.,...,.-..,.-,-,.,-.., ,-,.,-..-,-, ,..-.,..,.-..,., ,-,....,..,..., ,..,..., ,-,....,., ,-,.-.,.-,-.,...,.-..,.-,-,.,-.., ,--,---,.-.,...,., ,-.-.,---,-..,., ,-,.,-..-,-, ,..-.,..,.-..,., ,-,.-.,.-,-.,...,.-..,.-,-,.,-.., ,-,.-.,.-,-.,...,.-..,.-,-,.,-..', 'morse.wav')