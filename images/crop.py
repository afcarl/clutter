from os.path import isfile, join
from os import listdir
from PIL import Image 

path = "."
only_files = [f for f in listdir(path) if isfile(join(path, f))]

remove_top = 300
remove_bottom = 75

for f in only_files:
    if f.split('.')[-1] == "png":
        with Image.open(join(path, f)) as img:
            w, h = img.size
            img.crop((0, remove_top, w, h-75)).save(join(path,f))
