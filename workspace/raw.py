#!/usr/bin/env python3

# tail -c +13 temp.raw > rock.rgba
# adb exec-out screencap -p > auto_confirm.png

import os
import sys
import fire
import logging
import structlog
from logbook import Logger, StreamHandler
import numpy as np
from scipy.misc import imread, imshow, toimage
from PIL import Image

StreamHandler(sys.stdout).push_application()
log2 = Logger('Logbook')

log = structlog.get_logger()

def rawImage():
    log2.info('hello')
    log.msg("start")
    filename = 'temp.raw'
    os.system('adb shell screencap /sdcard/temp.raw')
    os.system('adb pull /sdcard/{0} &> /dev/null'.format(filename))

    bin_file = open(filename, 'rb')
    bin_file.seek(12)
    data = np.fromfile(bin_file, dtype=np.uint8)
    # data = np.fromfile('rock.rgba', dtype=np.uint8)
    r = data[::4].reshape((1920, 1080))
    g = data[1::4].reshape((1920, 1080))
    b = data[2::4].reshape((1920, 1080))
    r_im = Image.fromarray(r)
    g_im = Image.fromarray(g)
    b_im = Image.fromarray(b)
    im = Image.merge('RGB', (r_im, g_im, b_im))
    # r_im.save('pic.png')
    im.save('pic.png')
    log.msg('save png')
    log2.info('done')

def main():
    fire.Fire(rawImage)


if __name__ == '__main__':
    main()
