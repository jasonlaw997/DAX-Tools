
import win32con,win32gui
from time import sleep
import os

def send_msg_filter(handle,value):
    if handle !=123:
        menhandle = win32gui.FindWindowEx(handle, 0, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", "toolStrip2")
        # print(menhandle)
        filter_hwnd= win32gui.FindWindowEx(menhandle,None, "WindowsForms10.EDIT.app.0.ea7f4a_r7_ad1",None)
        # print(filter_hwnd)
        win32gui.SendMessage(filter_hwnd, win32con.WM_SETTEXT, None, value)
        win32gui.SendMessage(filter_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(filter_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


#=================================do not work
def send_msg_input(handle,value):

    # handle = win32gui.FindWindow("WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)

    t2_handle = win32gui.FindWindowEx(handle, 0, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t2_handle)
    t3_1_handle = win32gui.FindWindowEx(t2_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t3_1_handle)
    t3_2_handle = win32gui.FindWindowEx(t2_handle, t3_1_handle, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t3_2_handle)

    t4_handle = win32gui.FindWindowEx(t3_2_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t4_handle)

    t5_handle = win32gui.FindWindowEx(t4_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t5_handle)

    t6_handle = win32gui.FindWindowEx(t5_handle, None, "WindowsForms10.SysTabControl32.app.0.ea7f4a_r7_ad1", None)
    # print(t6_handle)

    t7_handle = win32gui.FindWindowEx(t6_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t7_handle)

    t8_1_handle = win32gui.FindWindowEx(t7_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    print("度量编辑框句柄：",t8_1_handle)

    # win32gui.SetForegroundWindow(t8_1_handle)
    win32gui.SendMessage(t8_1_handle, 770, 0, 0)

    # win32gui.SetForegroundWindow(t8_1_handle)
    # sleep(1)
    # win32gui.SendMessage(t8_1_handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # win32gui.SendMessage(t8_1_handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    title = win32gui.GetWindowText(t8_1_handle)
    print("度量编辑框 标题：",title)


    t8_2_handle = win32gui.FindWindowEx(t7_handle,t8_1_handle, "WindowsForms10.STATIC.app.0.ea7f4a_r7_ad1", None)
    print("度量名句柄：",t8_2_handle)

    xx = win32gui.GetWindowText(t8_2_handle)
    print("度量名：", xx)


    # print(win32gui.SendMessage(t8_1_handle, win32con.WM_GETTEXT, 0, value))

if __name__ == '__main__':
    t1_handle = win32gui.FindWindow("WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1",None)
    print(t1_handle)
    send_msg_input(t1_handle, "x333")

