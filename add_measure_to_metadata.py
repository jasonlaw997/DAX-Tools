import win32con, win32gui, win32api
from time import sleep
import pyperclip as clip
import ast


def get_measure(handle):
    # t1_handle = win32gui.FindWindow("WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t1_handle)
    # handle 是dax tools 绑定的 tabular editor 的句柄
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
    # print("度量编辑框句柄：",t8_1_handle)

    # win32gui.SetForegroundWindow(t8_1_handle)

    # win32gui.SetForegroundWindow(t8_1_handle)
    # sleep(1)
    # win32gui.SendMessage(t8_1_handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # win32gui.SendMessage(t8_1_handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    # title = win32gui.GetWindowText(t8_1_handle)
    # print("度量编辑框 标题：",title)

    t8_2_handle = win32gui.FindWindowEx(t7_handle, t8_1_handle, "WindowsForms10.STATIC.app.0.ea7f4a_r7_ad1", None)
    print("度量名句柄：", t8_2_handle)

    measure_name = win32gui.GetWindowText(t8_2_handle)[0:-2]
    # print(type(measure_name))
    print("度量名：", measure_name)

    return measure_name


def get_measure_enter(handle):
    t2_handle = win32gui.FindWindowEx(handle, 0, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    print(t2_handle, hex(t2_handle))
    t3_1_handle = win32gui.FindWindowEx(t2_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    print(t3_1_handle, hex(t3_1_handle))

    t4_handle = win32gui.FindWindowEx(t3_1_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    print(t4_handle, hex(t4_handle))
    t5_1_handle = win32gui.FindWindowEx(t4_handle, None, "WindowsForms10.SCROLLBAR.app.0.ea7f4a_r7_ad1", None)
    print(t5_1_handle, hex(t5_1_handle))

    t5_2_handle = win32gui.FindWindowEx(t4_handle, t5_1_handle, "WindowsForms10.EDIT.app.0.ea7f4a_r7_ad1", None)
    print(t5_2_handle, hex(t5_2_handle))
    text = win32gui.GetWindowText(t5_2_handle)
    measure_name="["+text +"]"
    print("度量名：", measure_name)

    return measure_name

def get_measure_enter2(handle):
    t2_handle = win32gui.FindWindowEx(handle, 0, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t2_handle, hex(t2_handle))
    t3_1_handle = win32gui.FindWindowEx(t2_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t3_1_handle, hex(t3_1_handle))

    t4_handle = win32gui.FindWindowEx(t3_1_handle, None, "WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    # print(t4_handle, hex(t4_handle))
    t5_1_handle = win32gui.FindWindowEx(t4_handle, None, "WindowsForms10.SCROLLBAR.app.0.ea7f4a_r7_ad1", None)
    # print(t5_1_handle, hex(t5_1_handle))

    t5_2_handle = win32gui.FindWindowEx(t4_handle, t5_1_handle, "WindowsForms10.EDIT.app.0.ea7f4a_r7_ad1", None)
    print(t5_2_handle, hex(t5_2_handle))
    measure_name = "1"  # flag
    if t5_2_handle != 0:
        sleep(0.2)
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(67, 0, 0, 0)  # c键位码是67
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        sleep(0.5)
        clip_data = clip.paste()
        try:
            mes_dict = ast.literal_eval(clip_data)
            # print(mes_dict)
            measure_name="["+mes_dict["measures"][0]["name"]+"]"
        except Exception as e:
            print(e)

    return measure_name




if __name__ == '__main__':
    t1_handle = win32gui.FindWindow("WindowsForms10.Window.8.app.0.ea7f4a_r7_ad1", None)
    print(t1_handle)
    get_measure_enter2(t1_handle)
    # get_measure_enter(t1_handle)
    # print(hex(t1_handle))
