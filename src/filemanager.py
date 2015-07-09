import os
import shutil

def move_file(filename, src, dest):
    src = os.path.join(src, filename)
    dest = os.path.join(dest, filename)
    shutil.move(src, dest)

def create_file(filename, path):
    filename = os.path.join(path, filename)
    f = open(filename, 'w+')
    f.close()

def delete_file(filename, path):
    filename = os.path.join(path, filename)
    os.remove(filename)

def delete_directory(directory):
    os.rmdir(directory)
