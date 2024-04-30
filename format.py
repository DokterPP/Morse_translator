class Format:
    def __init__(self):
        self.morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
        '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '_': '..--.-', '"': '.-..-.',
        '$': '...-..-', '@': '.--.-.'
        }
    
    def formatToMorse(self, message):
        encoded_message = ""
        for char in message:
            if char == '\n':
                encoded_message= encoded_message[:-1] # Remove last comma before newline
                encoded_message += "\n"  # Preserve newline breaks in encoded message
                continue
            encoded_char = self.__encode_character(self.morse_dict, char)
            #check if encoded_char is within the morse_dict
            if encoded_char == char:
                encoded_message += encoded_char
            else:
                encoded_message += encoded_char + ','
        return encoded_message


    def __encode_character(self, morse_dict, char):
        if char == ' ':
            return ' '  # Preserve spaces
        if char.upper() not in morse_dict:
            return char  # Character not supported
        return morse_dict[char.upper()]

    def formatToText(self, message):
        decoded_message = ""
        for char in message.split(','):
            if char == '\n':
                decoded_message= decoded_message[:-1] # Remove last comma before newline
                decoded_message += "\n"
                continue
            decoded_char = self.__decode_character(self.morse_dict, char)
            #check if decoded_char is within the morse_dict
            if decoded_char == char:
                decoded_message += decoded_char
            else:
                decoded_message += decoded_char
        return decoded_message
    
    def __decode_character(self, morse_dict, char):
        if char == ' ':
            return ' '
        for key, value in morse_dict.items():
            if value == char:
                return key
        return char
    
    def checkFile(self, file_contents):
        check = ""
        check += "Illegal characters denoted by (): \n\n"
        for char in file_contents:
            if char.upper() not in self.morse_dict and char.upper() not in [' ', '\n', ',']:
                check += "("+char+")"
            else:
                check += char
        return check
    
    def clearFile(self, file_contents):
        clear = ""
        for char in file_contents:
            if char.upper() not in self.morse_dict and char.upper() not in [' ', '\n', ',']:
                continue
            else:
                clear += char
        return clear