import os
from src import file_encode

# specify the directory you want to check. Use '.' for current directory
directory = "./src"

# get the list of all files and directories in the specified directory
files_in_directory = os.listdir(directory)

# print the list
print(files_in_directory)
