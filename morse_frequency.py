from datetime import datetime
from translation import MorseCodeTranslator
import os

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class SortedList:
    def __init__(self):
        self.head = None

    def insert(self, item):
        node = Node(item)
        if self.head is None or node.data < self.head.data:
            node.next = self.head
            self.head = node
        else:
            curr = self.head
            while curr.next is not None and curr.next.data < node.data:
                curr = curr.next
            node.next = curr.next
            curr.next = node

    def get_list(self):
        curr = self.head
        items = []
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def __str__(self):
        return ', '.join(str(item) for item in self.get_list())

class keyword:
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency

    def __lt__(self, other):
        if self.frequency == other.frequency:
            return self.word.lower() < other.word.lower()
        else:
            return self.frequency > other.frequency

    def __str__(self):
        return "'" + self.word + "': " + str(self.frequency)
    
class Morse_Frequency:
    def __init__(self):
        self.current_directory = os.path.dirname(__file__)
        
    #Read the Stop Words
    def read_stop_words(self, file_path):
        file_path = os.path.join(self.current_directory, file_path)
        with open(file_path, 'r') as file:
            return file.read().strip().split()

    # Count the frequencies of each Morse word
    def __count_word_frequencies(self, decoded_morse_text):
        word_frequencies = {}
        for word in decoded_morse_text.split():  # Split the text into words based on spaces
            if word not in word_frequencies:
                word_frequencies[word] = 0
            word_frequencies[word] += 1
        return word_frequencies


    # Identify keywords based on a list of stop words
    def __identify_keywords(self, word_frequencies, stop_words):
        # return the word frequencies that are not in the stop words list
        return {word: freq for word, freq in word_frequencies.items() if word.lower() not in stop_words}


    # Generate the Morse Word Frequencies Report

    def generate_report(self, decoded_morse, stop_words):
        if decoded_morse == None:
            return None
        # Time stamp
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        # Decoded morse text
        decoded_morse_text_section = "*** Decoded Morse Text\n" + (decoded_morse)

        # Count word frequencies 
        word_frequencies = self.__count_word_frequencies(decoded_morse)

       # Group and sort Morse words by frequencies and length of Morse code
        sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: (x[1], -len(MorseCodeTranslator().encode(x[0])), x[0]))
        grouped_word_frequencies = {}
        for word, freq in sorted_word_frequencies:
            if freq not in grouped_word_frequencies:
                grouped_word_frequencies[freq] = []
            grouped_word_frequencies[freq].append((word, freq))

        # Generate summary section
        summary_section = ""
        for freq, words in grouped_word_frequencies.items():
            summary_section += f"\n*** Morse Words with frequency=> {freq}\n"
            for word, _ in words:
                if word.lower() in stop_words:
                    keyword_label = ""
                else:
                    keyword_label = "(*)"
                # Convert word to morse code
                morse_code = MorseCodeTranslator().encode(word)
                summary_section += f"[{morse_code}]=> {word}{keyword_label}\n"


        # Identify keywords
        keywords = self.__identify_keywords(word_frequencies, stop_words)

        # Generate report for keywords sorted by frequency
        keywords_section = "*** Keywords sorted by frequency\n"
        sorted_keywords = sorted(keywords.items(), key=lambda x: (-x[1], x[0]))
        for word, freq in sorted_keywords:
            keywords_section += f"{word}({freq})\n"

        # Combine all sections to form the report
        report = f"""\
{"*" * 42}
   REPORT GENERATED ON: {timestamp}
{"*" * 42}

{decoded_morse_text_section}

{summary_section}
{keywords_section}
    """
        return report

    def generate_graph(self, decoded_morse, stop_words, words_linkedlist):
        # Time stamp

        words_linkedlist.set_list(words_linkedlist)  # Update the linked list properly
        
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        # Count word frequencies
        word_frequencies = self.__count_word_frequencies(decoded_morse)
        # Identify keywords
        keywords = self.__identify_keywords(word_frequencies, stop_words)
        
        # Remove words in the linked list that are not in the keywords
        words_linkedlist.remove_existence(stop_words)  # Pass stop_words to the method
        words_linkedlist.print_list(words_linkedlist)  # Print the updated linked list
        
        # Sort keywords by frequency
        # sorted_keywords = sorted(keywords.items(), key=lambda x: (-x[1], x[0])) 

        # testing sorted list using sorted list class
        l = SortedList()
        # Populate a list with keyword objects
        for word , frequency in keywords.items():
            l.insert(keyword(word, frequency))   
        keyword_frequencies = [item.frequency for item in l.get_list()]
        sorted_keywords = [item.word for item in l.get_list()]
 
 

        # Construct the graph
        graph = f"""\
{"*" * 60}
         REPORT GENERATED ON: {timestamp}
{"*" * 60}

"""     

        graph += self.print_vertical_bars(keyword_frequencies,words_linkedlist,sorted_keywords)
        return graph
    
    def print_vertical_bars(self, numbers,words_linkedlist,sorted_keywords):
        bar_print = "" 
        max_height = max(numbers)
        num_bars = len(numbers)
        total_spaces = 60 - num_bars  # base length is fixed at 60

        # Calculate the number of spaces between each bar
        if num_bars > 1:
            space_between_bars = total_spaces // (num_bars)
            remaining_spaces = total_spaces % (num_bars - 1)
        else:
            space_between_bars = 0
            remaining_spaces = total_spaces

        # Iterate through each position vertically
        for i in range(max_height, 0, -1):
            # Iterate through each number in the list

            for j, num in enumerate(numbers):
                if num >= i:
                    bar_print += "*"
                else:
                    bar_print += " "

                # Add extra spaces between bars
                if j < num_bars - 1:
                    num_spaces = space_between_bars + (1 if remaining_spaces > 0 else 0)
                    bar_print += " " * num_spaces
                    remaining_spaces -= 1 if remaining_spaces > 0 else 0

            # Move to the next line after printing each row
            bar_print += "\n"

        # Print fixed length base
        bar_print += "-" * 60 + "\n"

        words_linkedlist.sort_by_keywords(sorted_keywords)
        word_print =  words_linkedlist.report_generation_method()
        graph = bar_print + word_print

        return graph


 