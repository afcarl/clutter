from os.path import isfile, join
from os import listdir
from PIL import Image 

path = "."
only_files = [f for f in listdir(path) if isfile(join(path, f))]

for f in only_files:
    if f.split('.')[-1] == "png":
        with Image.open(join(path, f)) as img:
            w, h = img.size
            img.crop((150, 0, w-150, h)).save(join(path,f))
