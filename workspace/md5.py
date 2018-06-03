#!/usr/bin/env python3

import imageio
import fire
import hashlib
from scipy.spatial import distance


def md5(file1, file2):
    im1 = imageio.imread(file1, pilmode='RGB')
    im2 = imageio.imread(file2, pilmode='RGB')
    print(file1, hashlib.md5(im1.tobytes()).hexdigest())
    print(file2, hashlib.md5(im2.tobytes()).hexdigest())
    for i in [0, 1, 2]:
        print(i, distance.cosine(
            im1[:, :, i].flatten(), im2[:, :, i].flatten()))
    print()
    for i in [0, 1, 2]:
        print(i, distance.correlation(
            im1[:, :, i].flatten(), im2[:, :, i].flatten()))


def main():
    fire.Fire(md5)


if __name__ == '__main__':
    main()
