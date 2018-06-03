#!/usr/bin/env python3

import matplotlib.pyplot as plt
import fire


def show(filename):
    """show a image"""
    im = plt.imread(filename)
    plt.imshow(im)
    plt.show()

def main():
    fire.Fire(show)

if __name__ == '__main__':
    main()



