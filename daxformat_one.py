import threading
import time
import datetime
import win32api
import win32con
from time import sleep
import ctypes
import threading
import time
import  requests
import pyperclip as clip
from pynput.keyboard import Controller, Key, Listener
from tkinter import Label, Tk
import collections
import datetime

#摧毁弹窗
def worker():
    while True:
        title_list=["DAX error","timeout"]           #["succeed","DAX error","timeout"]
        for title in title_list:
            sleep(2)
            wd=ctypes.windll.user32.FindWindowA(0,title.encode('gb2312'))
            ctypes.windll.user32.SendMessageA(wd,0x0010,0,0)
        f12_state=win32api.GetAsyncKeyState(123) #123-f12的键位码,f12退出循环
        if f12_state==1:
            break
    return

def AutoCloseMessageBoxW(text, title):
    ctypes.windll.user32.MessageBoxA(0, text.encode('gb2312'), title.encode('gb2312'))



def Ctrl_X(key):
    if key=="v":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key=="a":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(65, 0, 0, 0)  # a键位码是65
        win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key=="c":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(67, 0, 0, 0)  # c键位码是67
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key=="ac":
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(65, 0, 0, 0)  # a键位码是65
        win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(67, 0, 0, 0)  # c键位码是67
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif key=="av":
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
    i=0
    Ctrl_X("ac")  # 全选复制
    sleep(1)
    while i<3:
        try:
            x = {'Dax': clip.paste(), 'ListSeparator': ',', 'DecimalSeparator': '.', 'MaxLineLenght': 0}
            url = 'https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'
            r = requests.post(url, data=x,timeout=5)
            dax_dict = r.json()
            # print(dax_dict)
            d1 = dax_dict["formatted"]
            if len(d1)==0:
                # print("DAX公式错误")
                AutoCloseMessageBoxW("DAX error", 'DAX error')

                break
            result = ""
            for i, v in enumerate(d1):
                if i > 0:
                    result = result + '\r\n'
                for x in v:
                    result = result + x["string"]
            # print(result)
            clip.copy(result) #结果存储到剪切板


            text="measure : "+d1[0][0]["string"][0:-1]+" --------has been formatted"
            print(text)
            Ctrl_X("av")
            # AutoCloseMessageBoxW(text, 'succeed')
            break
        except :
            i=i+1
            AutoCloseMessageBoxW("timeout", 'timeout')



def on_release(key):
    global  all_key

    if str(key)=="'\\x11'":     #"'\x03'"是Ctrl+C  "'\x11'"是Ctrl+Q  需要加一个转移符\
        all_key.append(str(key))
    if  len(all_key)>1:
        try:
            c = collections.Counter(all_key)
            c2=c["'\\x11'"]
            all_key.clear()
            if c2>=2 :
                time_str=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("start:"+time_str)
                get_dax()
        except:
            all_key.clear()
    else:
        if len(all_key)>1:
            print("on press key do not work")
        else:
            pass

    if key == Key.f12:
        return False


def start_listen():
    with Listener(on_press=None, on_release=on_release) as listener:
        listener.join()

def daxformat_main():
    global all_key
    all_key = []
    t = threading.Thread(target=worker, args=())
    # t.setDaemon(True)
    t.start()
    start_listen()
if __name__ == '__main__':
    # Ctrl+q+q 触发格式化
    # 开始监听,按f12退出监听
    daxformat_main()