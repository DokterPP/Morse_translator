"""
Name: Surya
Admin No.: P2100874
"""

from menu import Menu
from translation import MorseCodeTranslator
from file_process import file_access
from format import Format
from morse_frequency import Morse_Frequency
from colors import bcolors
from charmap_instance import dsCharmap
from audio import MorseCodeWav
from file_process import TextFileProcessor
from file_process import AudioFileProcessor



def main():
    """
    Use the Menu class to create a menu object
    """
    mainMenu = Menu(
        f"\n Please select your choice: ({','.join([str(x+1) for x in range(8)])})", True)
    mainMenu.showBanner()
    mainMenu.insert(["Convert Text To Morse Code",
                     "Convert Morse Code To Text",
                     "Generate Morse Word Frequencies Report",
                     "Generate Morse Keyword Frequencies Graph",
                     "Format File for Conversion (Advanced Options)",
                     "Dictionary Management (Advanced Options)",
                     "Morse Audio Conversion (experiment)",    
                     "Exit", ])
    input("Press Enter, to continue....")
    
    dsCharmap
    exitApp = False
    while not exitApp:
        choice = False
        while not choice:
            mainMenu.show() # Show main menu
            stop_words = Morse_Frequency().read_stop_words("stopwords.txt")
            choice = input("Enter choice: ")
            # Main menu validation
            if choice == '1':
                
                file_deet = TextFileProcessor().fileInput()
                morse = MorseCodeTranslator().encode(file_deet[0])
                file_access().fileOutput(morse, file_deet[1])
                
            elif choice == '2':
                
                file_deet = file_access().fileInput()
                text = MorseCodeTranslator().decode(file_deet[0])
                file_access().fileOutput(text, file_deet[1])
                
            elif choice == '3':
                
                file_deet = file_access().fileInput()
                text = MorseCodeTranslator().decode(file_deet[0])
                report = Morse_Frequency().generate_report(text, stop_words)
                file_access().fileOutput(report, file_deet[1], " Report")
                
            elif choice == '4':
                
                file_deet = file_access().fileInput()
                if MorseCodeTranslator().decode(file_deet[0], output_linkedlist=True) == None:
                    file_access().fileOutput(None, file_deet[1], " Graph")
                else: 
                    text,words_linkedlist = MorseCodeTranslator().decode(file_deet[0], output_linkedlist=True)
                    graph = Morse_Frequency().generate_graph(text, stop_words, words_linkedlist)
                    file_access().fileOutput(graph, file_deet[1], " Graph")
                
            elif choice == '5':
                # Advance Menu 1
                
                advanceMenu = Menu(
                    f"Please select your choice: ({','.join([str(x+1) for x in range(4)])})", True)
                advanceList = ["Prepare file for Morse to Text Conversion ( All Morse )", "Prepare file for Text to Morse Conversion ( All Text )","File illegal characters check","Back to Main Menu"]
                advanceMenu.insert(advanceList)
                advanceValid = False
                while not advanceValid:
                    advanceMenu.show()
                    advanceChoice = input("Enter choice: ")
                    # input validation
                    if advanceChoice == "4":
                        advanceValid = True
                        continue
                    elif advanceChoice.isnumeric() and advanceChoice not in ["1", "2", "3"]:
                        print(f"{bcolors.WARNING}\nOnly options between 1 to 4 are available. Please try again!{bcolors.ENDC}")
                        advanceValid = False
                        continue
                    elif advanceChoice not in ["1", "2", "3"]:
                        print(f"{bcolors.WARNING}\nYou must enter a number. Please try again!{bcolors.ENDC}")
                        advanceValid = False
                        continue
                    advanceValid = True

                    if advanceChoice == "1":
                        
                        file_to_be_formated = file_access().fileInput()
                        formated = Format().formatToMorse(file_to_be_formated[0])
                        file_access().fileOutput(formated, file_to_be_formated[1])
                        
                    elif advanceChoice == "2":
                        
                        file_to_be_formated = file_access().fileInput()
                        formated = Format().formatToText(file_to_be_formated[0])
                        file_access().fileOutput(formated, file_to_be_formated[1])
                        
                    elif advanceChoice == "3":
                        
                        checkMenu = Menu(
                        f"Please select your choice: ({','.join([str(x+1) for x in range(3)])})", True)
                        checkList = ["Check for Illegal characters in file", "Clear Illegal characters in file", "Back to Main Menu"]
                        checkMenu.insert(checkList)
                        checkValid = False
                        while not checkValid:
                            checkMenu.show()
                            checkChoice = input("Enter choice: ")
                            # input validation
                            if checkChoice == "3":
                                checkValid = True
                                continue
                            elif checkChoice.isnumeric() and checkChoice not in ["1", "2", "3"]:
                                print(f"{bcolors.WARNING}\nOnly options between 1 to 3 are available. Please try again!{bcolors.ENDC}")
                                checkValid = False
                                continue
                            elif checkChoice not in ["1", "2", "3"]:
                                print(f"{bcolors.WARNING}\nYou must enter a number. Please try again!{bcolors.ENDC}")
                                checkValid = False
                                continue
                            checkValid = True
                            
                            if checkChoice == "1":
                                
                                file_to_be_formated = file_access().fileInput()
                                check = Format().checkFile(file_to_be_formated[0])
                                file_access().fileOutput(check, file_to_be_formated[1])
                            
                            elif checkChoice == "2":
                                    
                                file_to_be_formated = file_access().fileInput()
                                formated = Format().clearFile(file_to_be_formated[0])
                                file_access().fileOutput(formated, file_to_be_formated[1])
                                
                            else:
                                print("\nInvalid Input. Please try again!")
                                advanceValid = False


            elif choice == '6':
                advanceMenu2 = Menu(
                    f"Please select your choice: ({','.join([str(x+1) for x in range(7)])})", True)
                advanceList2 = ["Add/Remove characters from dictionary", "Check character legality","Display Dictionary","Save current Dictionary","Reset to default dictionary","Change Dictionaries","Back to Main Menu"]
                advanceMenu2.insert(advanceList2)
                advanceValid2 = False
                while not advanceValid2:
                    advanceMenu2.show()
                    advanceChoice2 = input("Enter choice: ")
                    # input validation
                    if advanceChoice2 == "7":
                        advanceValid2 = True
                        continue
                    elif advanceChoice2.isnumeric() and advanceChoice2 not in ["1", "2", "3", "4", "5", "6", "7"]:
                        print(f"{bcolors.WARNING}\nOnly options between 1 to 7 are available. Please try again!{bcolors.ENDC}")
                        advanceValid2 = False
                        continue
                    elif advanceChoice2 not in ["1", "2", "3", "4", "5", "6", "7"]:
                        print(f"{bcolors.WARNING}\nYou must enter a number. Please try again!{bcolors.ENDC}")
                        advanceValid2 = False
                        continue
                    advanceValid2 = True

                    if advanceChoice2 == "1":
                        
                        addMenu = Menu(
                        f"Please select your choice: ({','.join([str(x+1) for x in range(3)])})", True)
                        addList = ["Add Character", "Remove Character", "Back to Main Menu"]
                        addMenu.insert(addList)
                        addValid = False
                        while not addValid:
                            addMenu.show()
                            addChoice = input("Enter choice: ")
                            # input validation
                            if addChoice == "3":
                                addValid = True
                                continue
                            elif addChoice.isnumeric() and addChoice not in ["1", "2", "3"]:
                                print(f"{bcolors.WARNING}\nOnly options between 1 to 3 are available. Please try again!{bcolors.ENDC}")
                                addValid = False
                                continue
                            elif addChoice not in ["1", "2", "3"]:
                                print(f"{bcolors.WARNING}\nYou must enter a number. Please try again!{bcolors.ENDC}")
                                addValid = False
                                continue
                            addValid = True
                            
                            if addChoice == "1":
                                dsCharmap.insert()
                                
                            if addChoice == "2":
                                dsCharmap.remove()
                                       
                    elif advanceChoice2 == "2":
                        dsCharmap.search()
                            
                    elif advanceChoice2 == "3":
                        dsCharmap.print_dict()
                        
                    elif advanceChoice2 == "4":
                        dsCharmap.update()
                                              
                    elif advanceChoice2 == "5":
                        dsCharmap.reset()
                        
                    elif advanceChoice2 == "6":
                        dsCharmap.change()
                        
            elif choice == '7':
                
                file_deet = AudioFileProcessor().fileInput()
                MorseCodeWav().convert_to_wav(file_deet[0], file_deet[1])
            
            elif choice == '8':
                print(
                    '\nBye, thanks for using ST1507 DSAA: MorseCode Message Analyzer\n')
                exit()
            elif choice.isnumeric():
                print(f"{bcolors.WARNING}\nOnly options between 1 to 8 are available. Please try again!{bcolors.ENDC}")
                choice = False
            else:
                print(f"{bcolors.WARNING}\nYou must enter a number. Please try again!{bcolors.ENDC}")
                choice = False
            
if __name__ == "__main__":
    main()
    