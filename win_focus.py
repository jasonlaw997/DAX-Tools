import win32gui
import time
def get_input_win():
    input_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    input_win_class = win32gui.GetClassName(win32gui.GetForegroundWindow())
    input_win_hwnd = win32gui.FindWindow(input_win_class,input_win_title)
    return input_win_hwnd

def set_input_win_focus(hwnd):
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(e)


def set_DG_focus():
    # time.sleep(0.1)
    hwnd_dg = win32gui.FindWindow( 'DAX Tools','DAX Tools')
    # print("DG:"+str(hwnd_dg))
    try:
        win32gui.SetForegroundWindow(hwnd_dg)
    except:
        print("set_DG_focus Error")
if __name__ == '__main__':
    time.sleep(1)
    input_hwnd=get_input_win()
    time.sleep(1)
    set_input_win_focus(input_hwnd)
    time.sleep(1)
    set_DG_focus()


