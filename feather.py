#!/usr/bin/env python3
# adb exec-out screencap -p > auto_confirm.png

from PIL import Image
from datetime import datetime
from timeit import default_timer as timer

import os
import sys
import pytesseract
import time
import logging
import shutil
import urllib.request

if sys.platform == 'darwin':
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
else:
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

logging.info('start')

criterion = [
    {"box": (250, 800, 520, 850), "content": 'First'},
    {"box": (320, 775, 440, 830), "content": 'Fight'},
    {"box": (520, 1215, 600, 1240), "content": 'Battle'},
    {"box": (380, 605, 490, 645), "content": 'Battle'},
    {"box": (50, 600, 350, 680), "content": 'STAGE'},
    {"box": (300, 750, 450, 800), "content": 'Close'},
]

codes_list = [
    {"key": "100000", "value": "tower"},
    {"key": "010000", "value": "battle-confirming"},
    {"key": "001000", "value": "battle-loaded"},
    {"key": "001100", "value": "auto-battle-confirming"},
    {"key": "001010", "value": "battle-finished"},
    {"key": "000001", "value": "reward"}
]

strategies = [
    {"value": "tower", "point": (380, 830)},
    {"value": "battle-confirming", "point": (387, 797)},
    {"value": "battle-loaded", "point": (565, 1237)},
    {"value": "auto-battle-confirming", "point": (400, 630)},
    {"value": "battle-finished", "point": (400, 630)},
    {"value": "reward", "point": (400, 780)}
]

cnt = 0
waiting_count = 0
history = []


def get_screenshot():
    os.system('adb shell input keyevent KEYCODE_WAKEUP')
    filename = '%s.jpg' % datetime.now().strftime("%Y%m%d-%H%M%S")
    # filename = 'pic.png'
    start = timer()
    os.system('adb exec-out screencap -p > %s' % filename)
    # urllib.request.urlretrieve('http://127.0.0.1:64959/device/01bf22f2c7d1a1cc/screenshot.jpg', filename)
    #urllib.request.urlretrieve(url, filename)
    end = timer()
    logging.info("screenshot take %s" % (end - start))
    # time.sleep(0.2)
    # return filename
    return filename


def check(im, c):
    im2 = im.crop(c['box'])
    content = pytesseract.image_to_string(im2)
    # logging.info(content)
    return c['content'] in content


def check_all(filename):
    im = Image.open(filename)
    return [check(im, c) for c in criterion]


def tap(x, y):
    os.system('adb shell input tap %d %d' % (x, y))


def afterBattle():
    global cnt
    cnt += 1
    logging.info("battle count: %d" % cnt)


def afterStartBattle():
    time.sleep(6)

def sleep(n):
    def fn():
        time.sleep(n)
    return fn

aspects = [
    {"key": "tower", "after": afterBattle},
    {"key": "auto-battle-confirming", "after": afterStartBattle},
    {"key": "battle-confirming", "after": sleep(1)}
]


def beforce(strategy):
    pass


def after(strategy):
    pass


def noop():
    pass


def run():
    global waiting_count
    # time.sleep(1)
    screen = get_screenshot()
    start = timer()
    result = check_all(screen)
    code = ''.join([str(int(i)) for i in result])
    end = timer()
    logging.info('ocr spent %s' % (end - start))
    # logging.info('codes = %s', code)
    try:
        strategy = next(filter(lambda x: x['key'] == code, codes_list), {"key": code, "value": "wait"})
        logging.info(strategy)
        shutil.move(screen, strategy['value'])
        point = next(
            filter(lambda x: x["value"] == strategy['value'], strategies), None)['point']
        tap(*point)
        aspect = next(
            filter(lambda x: x['key'] == strategy['value'], aspects), {"after": noop})
        aspect['after']()
        waiting_count = 0
    except:
        waiting_count += 1
        # print(waiting_count)


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
