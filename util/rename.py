import os
import shutil
import re

current_father_dir = os.path.dirname(__file__)

def walk(root_dir):
    count = 1
    for fname in os.listdir(root_dir):
        path = os.path.join(root_dir, fname)
        (_, tempfilename) = os.path.split(path)
        (_, extension) = os.path.splitext(tempfilename)
        new_name = re.findall(r'\\(.+)', root_dir)[0] + '_' + str(count) + extension
        os.rename(path, os.path.join(root_dir, new_name))
        count += 1
          

for fname in os.listdir(current_father_dir):
    path = os.path.join(current_father_dir, fname)
    if path == __file__:
        continue
    walk(path)