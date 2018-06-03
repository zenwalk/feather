#!/usr/bin/env python3

import numpy as np
import fire
import os
import shutil
import hashlib
import imageio

from glob import glob

def dispatch(dir):
    os.chdir(dir)
    files = glob('*crop.png')
    for f in files:
        im = imageio.imread(f)
        md5 = hashlib.md5(im.tobytes()).hexdigest()
        os.makedirs(md5, exist_ok=True)
        shutil.move(f, md5)
        print(f)

def main():
    fire.Fire(dispatch)

if __name__ == '__main__':
    main()


    


