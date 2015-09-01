#Folderlord
#This program takes an input text file and an optional path.
#Input files look like this:
"""
app/
    some_folder/
        __init__.py
        something.py
    another_folder/
        __init__.py
        thing.py
    __init__.py
"""
#If no path is provided, the program makes this in a subfolder in the current path.

import sys
import os
import glob

def createHierarchy(file_name, file_path=None):
    print "Opening template instructions in %s."%file_name
    file_hierarchy_text = open(file_name,"r").read()
    print "Received the following folder and file hierarchy instructions:"
    print file_hierarchy_text
    if file_path is None:
        print "No path has been supplied. Using current directory."
        file_path = os.getcwd()
    print "Starting operation in %s."%file_path
    file_hierarchy_list = file_hierarchy_text.split("\n")
    current_folder = file_path
    previous_indentation = 0
    is_at_top_folder = True
    for instruction in file_hierarchy_list:
        print "*"*10,"New Line","*"*10
        print instruction
        indentation = len(instruction) - len(instruction.lstrip())
        current_indentation = indentation
        instruction_text = instruction.strip()
        if "." in instruction_text:
            #Instruction to make a file.
            print "Asked to make a file entitled \"%s\" in \"%s\"."%(instruction_text,current_folder)
            file_handler = open(os.path.join(current_folder, instruction_text),"a")
            file_handler.close()
        elif "\\" in instruction_text:
            if is_at_top_folder or (current_indentation > previous_indentation):
                print "Asked to make a folder entitled \"%s\" in \"%s\"."%(instruction_text,current_folder)
                current_folder = os.path.join(current_folder,instruction_text[:instruction_text.find("\\")])
                os.mkdir(current_folder)
                is_at_top_folder = False
            elif current_indentation <= previous_indentation:
                print ""
                current_folder = os.path.abspath(os.path.join(current_folder,".."))
                print "Asked to make a folder entitled \"%s\" in \"%s\"."%(instruction_text,current_folder)
                current_folder = os.path.join(current_folder,instruction_text[:instruction_text.find("\\")])
                os.mkdir(current_folder)

            #else:

            #Instruction to make a folder.
        elif len(instruction_text) >0:
            print "*"*5
            print "Received an instruction to make a file or folder named \"%s\" in path: \"%s\". Unknown syntax."%(instruction_text, current_folder)
            print "*"*5

        previous_indentation = current_indentation



if __name__ == "__main__":
    file_name = sys.argv[1]
    if len(sys.argv) > 2:
        file_path = sys.argv[2]
    else:
        file_path = None
    createHierarchy(file_name, file_path)
