class MorseCodeTranslator:
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
        self.morse_tree = self.__build_morse_tree()

    class Node:
        def __init__(self, value):
            self.value = value
            self.children = {}

        def add_child(self, symbol, child):
            self.children[symbol] = child

    def __build_morse_tree(self):
        root = self.Node('')
        for char, code in self.morse_dict.items():
            current_node = root
            for symbol in code:
                if symbol not in current_node.children:
                    current_node.children[symbol] = self.Node('')
                current_node = current_node.children[symbol]
            current_node.value = char
        return root

    def encode(self, message):
        encoded_message = ""
        for char in message:
            if char == ' ':
                encoded_message += " ," 
                continue
            elif char == '\n':
                encoded_message = encoded_message[:-1]  # Remove last comma before newline
                encoded_message += "\n"  # Preserve newline breaks in encoded message
                continue
            encoded_char = self.__encode_character(char)
            if encoded_char is None:
                return None  # Character not supported
            encoded_message += encoded_char + ','
        return encoded_message[:-1]

    def __encode_character(self, char):
        if char == ' ' or char == '\n':
            return ''  # Return empty string for space or newline
        if char.upper() not in self.morse_dict:
            return None  # Character not supported
        return self.morse_dict[char.upper()]

    def decode(self, morse_code):
        lines = morse_code.split('\n')  # Split Morse code into lines based on newlines
        decoded_message = ""
        for line in lines:
            if not line.strip():  # Skip empty lines
                continue
            words = line.split()  # Split line into words based on whitespace
            for word in words:
                decoded_word = self.__decode_word(word.strip())
                if decoded_word is None:
                    return None  # Invalid Morse code
                decoded_message += decoded_word + ' '
            decoded_message += '\n'  # Add newline after each line
        return decoded_message.strip()

    def __decode_word(self, morse_word):
        decoded_word = ""
        characters = morse_word.split(',')  # Split Morse word into characters based on comma
        for char in characters:
            decoded_char = self.__decode_character(char.strip())
            if decoded_char is None:
                return None  # Invalid Morse code
            decoded_word += decoded_char
        return decoded_word

    def __decode_character(self, morse_code):
        current_node = self.morse_tree
        for symbol in morse_code:
            if symbol == '.':
                next_node = current_node.children.get('.', None)
            elif symbol == '-':
                next_node = current_node.children.get('-', None)
            else:
                return None  # Invalid Morse code
            if next_node is None:
                return None  # Invalid Morse code
            current_node = next_node
        return current_node.value
