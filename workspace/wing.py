
import logging
import os
import sys
from datetime import datetime
from functools import wraps
from time import sleep, time

import fire
import imageio
import numpy as np
import structlog
from logbook import Logger, StreamHandler
from PIL import Image

from globals import history
from imgHash import avhash, hamming

StreamHandler(sys.stdout).push_application()
logging = Logger('wing', level='INFO')

# FORMAT = "%(asctime)s %(levelname)s %(message)s"
# logging.basicConfig(format=FORMAT, level=logging.INFO)

logging.info('start')

cnt = 0
waiting_count = 0
# history = []



def timed(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logging.debug("{} ran in {}s".format(
            func.__name__, round(end - start, 2)))
        if func.__name__.startswith('get_screenshot'):
            return result, (end-start)
        else:
            return result
    return wrapper


def wake_up():
    os.system('adb shell input keyevent KEYCODE_WAKEUP')


def handle_raw():
    bin_file = open('temp.raw', 'rb')
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
    return im


@timed
def get_screenshot_raw():
    os.system('adb shell screencap /sdcard/temp.raw')
    os.system('adb pull /sdcard/temp.raw &> /dev/null')
    im = handle_raw()
    # r_im.save('pic.png')
    return im


@timed
def get_screenshot():
    filename = '%s.png' % datetime.now().strftime("%Y%m%d-%H%M%S")
    os.system('adb exec-out screencap -p > %s' % filename)
    # os.system('adb shell screencap /sdcard/temp.raw')
    # os.system('adb pull /sdcard/temp.raw')
    return filename


def expect(name, box, hash, retry=None):
    global cnt, waiting_count, history
    while True:
        im, consumed_time = get_screenshot_raw()
        history.append(consumed_time)
        im2 = im.crop(box)
        # im2.save('temp.png')
        h = hamming(avhash(im2), hash)
        # logging.info(f'h = {h}')
        if h <= 5:
            logging.info(f'expect {name} success')
            return
        else:
            if retry:
                tap(*retry)
            if len(history) > 50:
                logging.error(f'error maximum exceeded')
                exit()


def tap(x, y, delay=None):
    os.system('adb shell input tap %d %d' % (x, y))
    if delay:
        sleep(delay)


@timed
def run():
    global cnt, waiting_count, history
    # time.sleep(1)
    logging.info('round start')
    wake_up()
    history = []
    expect('lv5', (412, 1295, 500, 1340), 62990812538454016, (867, 417))
    tap(530, 1260)
    tap(570, 1200)
    sleep(1)
    expect('battle-loaded', (580, 1760, 725, 1900), 18446494484570112226)
    sleep(1)
    tap(840, 1835)
    tap(552, 942)
    # expect((580, 1760, 725, 1900), 18446742974197923840)
    # tap(552, 942)
    expect('reward', (171, 1096, 900, 1240), 72056494526332542, (541, 947, 2))
    tap(550, 1164)
    logging.info(f'screenshot count {len(history)}')
    logging.info(f'screenshot avg time {sum(history) / len(history)}')
    logging.info('round end')


def job():
    global cnt, waiting_count
    run()
    # if cnt > 10:
    #     exit()
    if waiting_count > 50:
        exit()


def main():
    while True:
        job()
        # time.sleep(0.5)


if __name__ == '__main__':
    main()
