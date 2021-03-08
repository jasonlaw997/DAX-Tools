import PySimpleGUI as sg
import win32api
import win32con
from time import sleep
import win32gui
import threading
import time
import requests
import pyperclip as clip
from pynput.keyboard import Key, Listener
import collections
import datetime
import random
import urllib3.contrib.pyopenssl
import os

import psutil

def kill_process_one():
    pidx=os.getpid()
    pids_list=psutil.pids()
    t1=0.01
    try:
        for p in pids_list:
            process=psutil.Process(p)
            # print(process)
            if process.name()=="daxformat_one_new.exe" and process.pid == pidx:
                # print(process.create_time())
                t1=process.create_time()
            if process.name() == "daxformat_one_new.exe":
                gap=t1-process.create_time()

                print(process.pid,process.name(),process.create_time(),gap)
                if abs(gap)>2:
                    process.kill()
    except Exception as e:
        print(e)

def Ctrl_X(key):
    if key == "v":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key == "a":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(65, 0, 0, 0)  # a键位码是65
        win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key == "c":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(67, 0, 0, 0)  # c键位码是67
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key == "ac":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(65, 0, 0, 0)  # a键位码是65
        win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(67, 0, 0, 0)  # c键位码是67
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    elif key == "av":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(65, 0, 0, 0)  # a键位码是65
        win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


# 键盘按压
def on_press(key):
    pass

def get_dax():
    Ctrl_X("ac")  # 全选复制
    sleep(0.3)
    # urllib3.contrib.pyopenssl.inject_into_urllib3()
    # requests.packages.urllib3.disable_warnings()
    # requests.adapters.DEFAULT_RETRIES = 3
    # session = requests.session()
    # session.keep_alive = False
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 '
        '(maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
        '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}               #, 'Connection': 'close'}
    url = 'https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'
    x = {'Dax': clip.paste(), 'ListSeparator': ',', 'DecimalSeparator': '.', 'MaxLineLenght': 0}
    r = requests.post(url, data=x, timeout=12, headers=headers)
    dax_dict = r.json()
    print(dax_dict)
    d1 = dax_dict["formatted"]
    if len(d1) == 0:
        # print("DAX公式错误")
        sg.popup_auto_close('DAX Error', auto_close_duration=2)
    else:
        result = ""
        for i, v in enumerate(d1):
            if i > 0:
                result = result + '\r\n'
            for x in v:
                result = result + x["string"]
        # print(result)
        clip.copy(result)  # 结果存储到剪切板
        text = "measure : " + d1[0][0]["string"][0:-1] + " --------has been formatted"
        print(text)
        Ctrl_X("av")



def on_release(key):
    global all_key
    input_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    win_title_list = ["Power BI Desktop", "记事本", "Microsoft Visual Studio", "PyCharm"]
    if any(win_title_name in input_win_title for win_title_name in win_title_list):
        if str(key) == "'\\x11'":                   # "'\x03'"是Ctrl+C  "'\x11'"是Ctrl+Q  需要加一个转移符\
            all_key.append(str(key))
        if len(all_key) > 1:
            try:
                c = collections.Counter(all_key)
                c2 = c["'\\x11'"]
                all_key.clear()
                if c2 >= 2:
                    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("start:" + time_str)
                    get_dax()
            except:
                all_key.clear()
        else:
            if len(all_key) > 1:
                print("on press key do not work")
            else:
                pass

    # if key == Key.f12:
    if str(key) == "'\\x17'":
        return False


def start_listen():
    pidx = os.getpid()
    print(222,pidx)
    with Listener(on_press=None, on_release=on_release) as listenerX:
        listenerX.join()


def daxformat_main():
    global all_key
    all_key = []
    kill_process_one()  #保证运行一个
    # Ctrl+q+q 触发格式化
    # 按Ctrl+w退出监听
    t = threading.Thread(target=start_listen, args=())
    n = 0
    while True:
        try:
            rcode = requests.get('http://www.baidu.com').status_code   #检查网络
            # print(rcode)
            if n > 0:
                sg.popup_auto_close('Network Available ', auto_close_duration=8)
            t.start()
            break
        except Exception as e:
            # print(e)
            sg.popup_auto_close('No Network', auto_close_duration=8)
            n = n + 1
            time.sleep(4)
            if n == 4:
                sg.popup_auto_close('The program will exit after 5 seconds', auto_close_duration=5)
                os._exit(0)


if __name__ == '__main__':
    # Ctrl+q+q 触发格式化
    # 按Ctrl+w退出监听
    sg.popup_auto_close('start', auto_close_duration=1.5)
    daxformat_main()


