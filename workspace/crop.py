#!/usr/bin/env python3

import os
import fire

from PIL import Image
from glob import glob

box = (0, 1160, 768, 1280)
box = (675, 20, 760, 100) # three color box
box = (400, 20, 480, 100)
box = (300, 1180, 700, 1280)
# box = (140, 750, 640, 950)
# box = (250, 620, 500, 720)
box = (0, 1200, 768, 1280)
box = (412, 1295, 500, 1340)
box = (580, 1760, 725, 1900)
box = (171, 1096, 900, 1240)


def crop(dir):
    os.chdir(dir)
    files = glob('c*.png')
    for f in files:
        im = Image.open(f)
        im = im.crop(box)
        im.save(f[:-4]+'crop'+'.png')
        print(f)
    return


def main():
    fire.Fire(crop)


if __name__ == '__main__':
    main()
