class LinkedList_Node:
    def __init__(self, morse_code, word):
        self.morse_code = morse_code
        self.word = word
        self.next = None
    
class MorseCodeLinkedList:
    linkedlist = None
    def __init__(self):
        self.head = None
        
    def set_list(self, list):
        MorseCodeLinkedList.linkedlist = list
    
    def get_individual_morse_code_total(self):
        current = self.head
        max_size = 0
        while current:
            for morse_code_char in current.morse_code:
                max_size += 1
            current = current.next
        return max_size

    def get_size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
            
    
    def add_node(self, morse_code, word):
        new_node = LinkedList_Node(morse_code, word)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            
    def report_generation_method(self):
        current = self.head
        num_bars = self.get_size()
        output_line = ""
        total_spaces = 60 
        
        # Iterate through each Morse code-word pair position
        for i in range(self.get_individual_morse_code_total()):
            current = self.head  # Reset current to the head of the linked list
            output_line = ""
            num_bars = self.get_size()
            #calculate space between bars
            space_between_bars = total_spaces // (num_bars)
            
            # Iterate through the linked list to build the output line
            while current:
                morse_length = len(current.morse_code)
                word_length = len(current.word)
                flag = False
                # Concatenate the Morse code and word pair if within the range, otherwise add empty space
                if i < morse_length and i < word_length:
                    output_line += f"{current.morse_code[i]}{current.word[i]}"
                    flag = True
                elif i < morse_length:
                    output_line += f"{current.morse_code[i]}"
                elif i < word_length:
                    output_line += f"{current.word[i]}"
                #check for no morse code or word
                else:
                    output_line += " "
                
                if flag == True:
                    output_line += " " * (space_between_bars - 1)
                else: 
                    output_line += " " * space_between_bars   # Add spaces between bars
                
                current = current.next  # Move to the next node
                
            # Print the output line
            print(output_line)
                

        
            
        
            
    # access word portion of linked list
    def remove_existence(self, stop_words):
        # Iterate through linked list and remove words that are not in stop_words
        current = self.head
        prev = None
        while current:
            if current.word.lower() not in stop_words:
                prev = current
                current = current.next
            else:
                # Remove word
                if current == self.head:
                    print("removing head")
                    self.head = current.next
                    current = self.head
                else:
                    print("removing word")
                    prev.next = current.next
                    current = prev.next

        # Make sure to update linkedlist.head if the head was removed
        MorseCodeLinkedList.linkedlist = self

    
    
    def print_list(self,linkedlist):
        current = linkedlist.head
        while current:
            print(f"{current.morse_code} => {current.word}")
            current = current.next
            


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
        
        def get_child(self, symbol):
            return self.children.get(symbol, None)


        
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

    def decode(self, morse_code, output_linkedlist = False):
        lines = morse_code.split('\n')  # Split Morse code into lines based on newlines
        decoded_message = ""
        if output_linkedlist:
            morse_linkedlist = MorseCodeLinkedList()
        #add decoded word and morse code to linked list if output_linkedlist is True
        
        for line in lines:
            if not line.strip():
                continue
            words = line.split()
            for word in words:
                decoded_word = self.__decode_word(word.strip())
                if decoded_word is None:
                    return None
                decoded_message += decoded_word + ' '
                if output_linkedlist:
                    morse_linkedlist.add_node(word, decoded_word)
            decoded_message += '\n'
        if output_linkedlist:
            return decoded_message,morse_linkedlist
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
