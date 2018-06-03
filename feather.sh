# adb exec-out screencap -p > myimg.png

adb shell input tap 568 1227  # click first floor
sleep 1
adb shell input tap 611 1230 # click start battle
sleep 10
adb shell input tap 833 1845 # click auto battle
sleep 2
adb shell input tap 543 974 # click ok
sleep 20
adb shell input tap 543 974 
sleep 10
adb shell input tap 555 1175
sleep 1
adb shell input keyevent KEYCODE_WAKEUP
