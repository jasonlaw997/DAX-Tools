import copy
from time import sleep

import win32gui,win32con,win32api
import win32clipboard

def input_value(value):
    global input_flag2
    input_flag2 = "y"
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT,value)
    # 获取剪贴板内容
    sleep(0.1)
    # date = win32clipboard.GetClipboardData()

    #因为backspace键会影响输入的字符串，所以需要向左移动一格，再用delete删除，起始的符合" ' "和 " ` "
    win32clipboard.CloseClipboard()
    # sleep(0.1)
    win32api.keybd_event(37, 0, 0, 0)  # 左方向键
    win32api.keybd_event(37, 0, win32con.KEYEVENTF_KEYUP, 0)# 释放按键

    win32api.keybd_event(46, 0, 0, 0)  # delete键
    win32api.keybd_event(46, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    # sleep(0.1)


    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


if __name__ == '__main__':
    sleep(2)
    value="sheetss"
    input_value(value)