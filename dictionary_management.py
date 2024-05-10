import json
import re

class Charmap:
    def __init__(self):
        self.arr = []
        self.map = {}
        self.size=0
        self.data = self.read_dict('dictionary.json')
        self.variables()
    
        
    def variables(self):
        self.dict = self.data['Dict']
        self.custom = self.data['Custom']
        self.fill_dict(self.dict)
        
    
    def read_dict(self, file):
        folder_path = 'dictionaries/'
        with open(folder_path+file, 'r') as file:
            data = json.load(file)
        return data
    
    def write_dict(self, file, data):
        folder_path = 'dictionaries/'
        with open(folder_path+file, 'w') as file:
            json.dump(data, file)
    
    def fill_dict(self ,data):
        for key, value in data.items():
            self.mass_insert(key, value)
        
    def mass_insert(self, char, morse):
        char = char.upper()
        if char not in self.map:
            index = self.size
            self.arr.append((char, morse))
            self.size+=1
            self.map[char] = index
        self.sort()

    def insert(self):
        # Check if the dictionary is advanced and prevent adding characters to it
        if self.data == self.read_dict('advanced_dict.json'):
            print("\nYou cannot add characters to the Advanced Dictionary.")
            input('\n'+"Press Enter, to continue....")
        else:
            while True:
                char = input("\nEnter character to add: ")
                if not re.match("^[A-Za-z!?@#$%&*()+=]$", char):
                    print("Invalid input. Please enter a single character.")
                    continue
                char = char.upper()
                if char in self.map:
                    print(f"\n'{char}' already exists in the dictionary.")
                    input('\n'+"Press Enter, to continue....")
                    continue
                morse = input("Enter morse code: ")
                if not re.match("^[.-]+$", morse):
                    print("Invalid input. Morse code can only contain dots (.) and dashes (-).")
                    continue
                index = self.size
                self.arr.append((char, morse))
                self.size += 1
                self.map[char] = index

                self.sort()
                input('\n'+"Press Enter, to continue....")
                break

    def remove(self):
        # Check if the dictionary is advanced and prevent adding characters to it
        if self.data == self.read_dict('advanced_dict.json'):
            print("\nYou cannot remove characters in the Advanced Dictionary.")
            input('\n'+"Press Enter, to continue....")
        else:
            while True:
                char = str(input("\nEnter character to remove: "))
                if char in self.map:
                    removed = False
                    while True:
                        confirm = str(input(f"\nAre you sure you want to remove {char}? (y/n): "))
                        if confirm.lower() == 'y':
                            index = self.map[char]
                            del self.map[char]
                            if index != self.size - 1:
                                last = self.size - 1
                                self.arr[index], self.arr[last] = self.arr[last], self.arr[index]
                                if last != index:
                                    self.map[self.arr[index][0]] = index
                            self.arr.pop()
                            self.size -= 1
                            self.sort()
                            removed = True
                            self.custom = "True"
                            break
                        elif confirm.lower() == 'n':
                            break
                        else:
                            print("\nInvalid input. Please enter 'y' or 'n'.")
                    if removed or confirm.lower() != 'y':
                        input('\n'+"Press Enter, to continue....")
                        break
                else:
                    print(f"\nThe character {char} does not exist.")
                    while True:
                        retry = str(input("\nDo you want to try again? (y/n): "))
                        if retry.lower() in ['y', 'n']:
                            break
                        else:
                            print("\nInvalid input. Please enter 'y' or 'n'.")
                    if retry.lower() == 'n':
                        input('\n'+"Press Enter, to continue....")
                        break
                
    def update(self):
        if self.data == self.read_dict('advanced_dict.json'):
            print("\nYou cannot save the Advanced Dictionary.")
            input('\n'+"Press Enter, to continue....")
        else:
            self.data['Dict'] = {k: v for k, v in self.arr}
            self.data['Custom'] = self.custom
            # Write updated data back to the JSON file
            self.write_dict('dictionary.json', self.data)
            print("\nDictionary updated successfully.")
            input('\n'+"Press Enter, to continue....")
    
    def sort(self):
        # Bubble sort
        for i in range(self.size):
            for j in range(0, self.size - i - 1):
                if self.arr[j][0] > self.arr[j + 1][0]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                    self.map[self.arr[j][0]], self.map[self.arr[j + 1][0]] = j, j + 1
                               
    def search(self):
        char = input("\nEnter character to check: ")
        char = char.upper()
        index = self.map.get(char, None)
        if index is not None:
            print(f"\nstatus:\n\nEXISTS\n\n'{self.arr[index][0]}' : '{self.arr[index][1]}'")
            input('\n'+"Press Enter, to continue....")
        else:
            print("status:\n\nDOES NOT EXIST")
            input('\n'+"Press Enter, to continue....")
            
    def print_dict(self):
        count = 0
        print('\n')
        for char, morse in self.arr:
            print(f'{char : <3} : {morse : <7}', end='  ')
            count += 1
            if count % 4 == 0:
                print('\n')
        if count % 4 != 0:
            print()  # Ensure the last line ends with a newline
        input('\n'+"Press Enter, to continue....")
        
    def reset(self):
        if self.data == self.read_dict('advanced_dict.json'):
            print("\nYou cannot reset the Advanced Dictionary.")
            input('\n'+"Press Enter, to continue....")
        else:
            while True:
                confirm = input("\nWARNING: This will reset the dictionary to its original state. Are you sure you want to continue? (y/n): ")
                if confirm.lower() == 'y':
                    # Reset the dictionary to its original state by copying from dictionary_default.json
                    data = self.read_dict('dictionary_default.json')
                    self.write_dict('dictionary.json', data)
                    self.__init__()
                    print("\nDictionary reset successfully.")
                    input('\n'+"Press Enter, to continue....")
                    break
                elif confirm.lower() == 'n':
                    break
                else:
                    print("\nInvalid input. Please enter 'y' or 'n'.")
            
    def change(self):
        while True:
            print("\nCurrent Dictionary:")
            if self.data == self.read_dict('dictionary.json'):
                print("Basic Dictionary")
            elif self.data == self.read_dict('advanced_dict.json'):
                print("Advanced Dictionary")
            else:
                print("Custom Dictionary")

            print("\n Select the dictionary you want to switch to:")
            print("\n\t1. Basic Dictionary")
            print("\t2. Advanced Dictionary (not editable)")
            choice = input("\nSelect the dictionary you want to switch to : ")
            if choice == '1':
                self.arr = []
                self.map = {}
                self.size=0 
                self.data = self.read_dict('dictionary.json')
                self.variables()
                print("\nSwitched to Basic Dictionary.")
                input('\n'+"Press Enter, to continue....")
                break
            elif choice == '2':
                self.arr = []
                self.map = {}
                self.size=0 
                self.data = self.read_dict('advanced_dict.json')
                self.variables()
                print("\nSwitched to Advanced Dictionary.")
                input('\n'+"Press Enter, to continue....")
                break
            else:
                print("\nInvalid input. Please enter 1 or 2.")
            #it is possible to allow a user to switch to a custom dictionary, but it is not implemented in this version