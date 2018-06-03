#!/usr/bin/env python3

import fire
import os
import shutil
from glob import glob


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def move(dir, n=100):
    """move n files to a new dir"""
    os.chdir(dir)
    files = glob('*.jpg')
    data = chunks(files, n)
    for idx, value in enumerate(data, 1):
        new_dir = str(idx)
        os.makedirs(new_dir, exist_ok=True)
        for file in value:
            shutil.move(file, new_dir)
            print(file)


def main():
    fire.Fire(move)


if __name__ == '__main__':
    main()
