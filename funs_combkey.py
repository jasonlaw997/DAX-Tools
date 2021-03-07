from pynput import keyboard
import win32api,win32con,win32gui,win32clipboard
from time import sleep
from threading import Lock
import pyperclip as clip

paste_lock=Lock()

shortcut_key_text_dict={
    "CALCULATE":'<caps_lock>+c',
    "SELECTEDVALUE":'<caps_lock>+s',
    "TREATAS":'<caps_lock>+t',
    "KEEPFILTERS":'<caps_lock>+k',
    "VALUES":'<caps_lock>+v',
    "FILTER":'<caps_lock>+f',
    "DISTINCT":'<caps_lock>+d',
    "EVALUATE":'<caps_lock>+e',
    "RETURN":'<caps_lock>+r',
    "SELECTEDMEASURE":'<caps_lock>+[',
    "SELECTEDMEASURENAME":'<caps_lock>+]'
}

shortcut_key_text="""
    CALCULATE : <caps_lock>+c 
    SELECTEDVALUE :<caps_lock>+s
    TREATAS :<caps_lock>+t 
    KEEPFILTERS : <caps_lock>+k
    VALUES : <caps_lock>+v
    FILTER : <caps_lock>+f
    DISTINCT : <caps_lock>+d'
    EVALUATE : <caps_lock>+e'
    RETURN : <caps_lock>+r'
    SELECTEDMEASURE : <caps_lock>+[
    SELECTEDMEASURENAME : <caps_lock>+]
    """

def paste_funs(value):
    input_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    input_win_class = win32gui.GetClassName(win32gui.GetForegroundWindow())
    input_win_hwnd = win32gui.FindWindow(input_win_class, input_win_title)
    win_title_list = ["Power BI Desktop", "Tabular Editor", "记事本", "Microsoft Visual Studio", "PyCharm"]
    if any(win_title_name in input_win_title for win_title_name in win_title_list):
        win32gui.SetForegroundWindow(input_win_hwnd)
        # sleep(0.1)
        # print(value)
        try:
            win32clipboard.CloseClipboard()
        except:
            None
        try:
            # win32clipboard.OpenClipboard()
            # win32clipboard.EmptyClipboard()
            # win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, value)
            # win32clipboard.CloseClipboard()

            clip.copy(value)
            sleep(0.1)


            win32api.keybd_event(8, 0, 0, 0)  # backspace
            win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)

            win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
            sleep(0.1)
            win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
            win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

            win32api.keybd_event(37, 0, 0, 0)  #left arrow
            win32api.keybd_event(37, 0, win32con.KEYEVENTF_KEYUP, 0)
        except Exception as e:
            print(e)


#
def on_f_calculate():
    paste_funs("CALCULATE( )")


def on_f_selectedvalue():
    paste_funs("SELECTEDVALUE( )")

def on_f_treatas():
    paste_funs("TREATAS( )")

def on_f_keepfilters():

    paste_funs("KEEPFILTERS( )")

# def on_f_values():
#     paste_funs("VALUES(")

def on_f_filter():
    paste_funs("FILTER( )")

def on_f_distinct():
    paste_funs("DISTINCT( )")
def on_f_evaluate():
    paste_funs("EVALUATE")

def on_f_selectedmeasure():
    paste_funs("SELECTEDMEASURE( )")

def on_f_selectedmeasurename():
    paste_funs("SELECTEDMEASURENAME( )")

def on_f_selectedeasureformatstring():
    paste_funs("SELECTEDEASUREFORMATSTRING( )")

def on_f_return():
    paste_funs("RETURN")

def  funs_combkey_listener():
    global shortcut_key_listener
    with keyboard.GlobalHotKeys({
    '<caps_lock>+c': on_f_calculate,
    '<caps_lock>+s': on_f_selectedvalue,
    '<caps_lock>+t': on_f_treatas,
    '<caps_lock>+k': on_f_keepfilters,
    # '<caps_lock>+v': on_f_values,
    '<caps_lock>+f': on_f_filter,
    '<caps_lock>+d': on_f_distinct,
    '<caps_lock>+e': on_f_evaluate,
    '<caps_lock>+r': on_f_return,
    '<caps_lock>+[': on_f_selectedmeasure,
    '<caps_lock>+]': on_f_selectedmeasurename
    }) as shortcut_key_listener:
     shortcut_key_listener.join()

if __name__ == "__main__":
    funs_combkey_listener()