import time
from  pynput.mouse import Button
from pynput.keyboard import Controller, Key
from pynput.keyboard import Listener as Keyboard_Listener
from pynput.mouse import Listener as Mouse_Listener
import os
from threading import Thread
from time import sleep
import win32api,win32con,win32gui,win32clipboard


def on_click(x, y , button, pressed):
    if pressed:  # 点击时为ture  如果不进行判断会调用两次这个函数 一次点击一次释放 这里不需要两次
        global click_count
        global time_difference  # 把时间差设为全局变量 为的是退出这个循环

        t = time.time()  # 获取当前电脑时间
        click_time.append(t)  # 添加时间
        click_location.append((x, y))  # 添加位置

        if len(click_location) != 1:  # 这几个判断以及上面定义的click_ 都是为了得到双击还是单击  两个list长度都是2 第一个和第二个比较时间差
            time_difference = click_time[1] - click_time[0]  # 定义时间差
            if click_location[0] == click_location[1]:
                if time_difference <= 0.3:  # 如果两次点击时间小于0.3秒就会判断为双击 否则就是单击
                    click_count = 2
                else:
                    click_count = 1
            else:
                click_count = 1
            click_time.pop(0)  # 删去第一个
            click_location.pop(0)
        if button == Button.left and click_count==2:  # 判断左键还是右键还是中键
            print(2222222)
            sleep(0.1)
            print("鼠标左键双击")
            win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
            win32api.keybd_event(67, 0, 0, 0)  # v键位码是86
            win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            sleep(0.1)
            win32clipboard.OpenClipboard()
            clip_data = win32clipboard.GetClipboardData()
            print(clip_data)
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
                # q_mouse_click.put(clip_data)
        elif button == Button.left and click_count==1 :
            if button == Button.left:  # 判断左键还是右键还是中键
                print("鼠标左键单击")


        if 'Key.esc' in all_key:
            # 在按下esc时将不再监控鼠标
            return False

if __name__=='__main__':
    global all_key  #获取按键信息

    click_location = []
    time_difference = 0
    click_count = 1
    click_time = []
    all_key = []
    mouse_listen_thread = Mouse_Listener(on_click=on_click)
    mouse_listen_thread.start()
    mouse_listen_thread.join()
