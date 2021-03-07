from win32gui import *

def foo(hwnd,titles):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))
def get_all_win_title():
    titles = set()
    EnumWindows(foo, titles)
    lt = [t for t in titles if t]
    lt.sort()
    return lt
if __name__ == '__main__':
    r=get_all_win_title()
    for i in r:
        print(i)
    print(r)