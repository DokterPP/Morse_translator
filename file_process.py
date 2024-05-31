import os
from colors import bcolors

    

class file_access:
    
    def __init__(self):
            self.current_directory = os.path.dirname(__file__)

    def processRead(self, file_input_path):
        try:
            # Open the file in read mode
            with open(file_input_path, 'r') as file:
                # Read all contents of the file into a string
                file_contents = file.read()
                return file_contents
        except FileNotFoundError:
            print(f"{bcolors.FAIL}Error: The file '{file_input_path}' does not exist.{bcolors.ENDC}")
            return None
        except Exception as e:
            print(f"{bcolors.FAIL}An error occurred: {str(e)} {bcolors.ENDC}")
            return None
        
    def fileOutput(self, file_contents, output_file_name, confirm_message=None):
        try:
            # Open the file in write mode
            with open(output_file_name, 'w') as file:
                # Write the contents to the file
                if file_contents == None:
                    print(f"{bcolors.FAIL}\nFile processing failed. Please check the input file contents. Illegal characters found or wrong text file used. Use file checker to check for illegal characters.{bcolors.ENDC}")
                    file_contents = "File processing failed. Please check the input file contents. Illegal characters found or wrong text file used. Use file checker to check for illegal characters."
                    file.write(file_contents)
                    self.__confirm()
                else:
                    file.write(file_contents)
                    self.__confirm(confirm_message)
        except Exception as e:
            print(f"{bcolors.FAIL}\nAn error occurred: {str(e)} {bcolors.ENDC}")
            return None      
    
    def __confirm(self, message=None):
        if message is not None:
            print('\n'+ ">" * 4 + message + " generation completed! " +"\n")
        input('\n'+"Press Enter, to continue....")
        
    
    def fileInput(self, audio): 
            while True:
                # Prompt for input file name
                input_file_name = input('\n'+"Please enter input file name: ")
                file_input_path = os.path.join(self.current_directory, input_file_name)

                # Check if input file exists and is a .txt file
                if os.path.exists(file_input_path) and input_file_name.endswith('.txt'):
                    # Process input file contents
                    file_contents = self.processRead(file_input_path)
                    if file_contents is not None:
                        # Prompt for output file name
                        while True:
                            output_file_name = input("Please enter output file name: ")
                            if audio == True :
                                if output_file_name.endswith('.wav'):
                                    output_file_path = os.path.join(self.current_directory, output_file_name)
                                    return file_contents, output_file_path
                                else:
                                    print(f"{bcolors.WARNING}\nInvalid output file name. Output file must end with .wav.{bcolors.ENDC}")     
                            elif output_file_name.endswith('.txt'):
                                output_file_path = os.path.join(self.current_directory, output_file_name)
                                return file_contents, output_file_path
                            else:
                                print(f"{bcolors.WARNING}\nInvalid output file name. Output file must end with .txt.{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.FAIL}\nFile processing failed. Please check the input file contents.{bcolors.ENDC}")
                else:
                    print(f"{bcolors.WARNING}\nInvalid input file name or file does not exist. Please enter a valid .txt file.{bcolors.ENDC}")
                   
class TextFileProcessor(file_access):
    def fileInput(self):
            return super().fileInput(audio = False)

class AudioFileProcessor(file_access):
     def fileInput(self):
            return super().fileInput(audio = True)

        

