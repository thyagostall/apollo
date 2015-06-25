import os
import shutil

def move_files(files, src, dest):
    for file_name in files:
        file_name = os.path.join(src, file_name)
        shutil.move(file_name, os.path.join(dest, file_name))

def create_file(filename):
    f = open(filename, 'w+')
    f.close()

def create_files(files, path):
    for file_name in files:
        create_file(os.join([path, file_name]))

def delete_files(files):
    for file_name in files:
        os.remove(file_name)

def delete_directory(directory):
    os.rmdir(directory)
