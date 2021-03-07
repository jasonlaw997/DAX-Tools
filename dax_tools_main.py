import sys
import os
import pyperclip as clip
from pynput.keyboard import Controller, Key, Listener
import threading
from dearpygui.core import *
from dearpygui.simple import *
# from daxformat_one_new import daxformat_main
from time import sleep
import time
import ctypes
import win32con
import win32api
import win32gui
import copy
import json
import re
import webbrowser
from get_metadata import *
from get_bim_metadata import *
from win_focus import *
from queue import Queue
from funs_data_list import *
from format_all import *
from funs_combkey import *
from get_win_title import *
from threading import Lock
from gui_solution_dict import *
from send_filter_value import *
from add_measure_to_metadata import *

global all_key, q_cv_info

clip_lock = Lock()
input_lock = Lock()

q_cv_info = Queue()
click_location = []
time_difference = 0
click_count = 1
click_time = []
all_key = []
thread_key_mouse_flag = 'y'

global q
q = Queue()  # 传递输入文本给展示table
q_input = Queue()  # 传递inupt框的输入文本


def add_measure(kk):
    global meta_dict, edit_hwnd
    if edit_hwnd != 123:
        if kk == "space":
            xx= get_measure(edit_hwnd)
            name=xx.strip()
        elif kk == "enter":
            name = get_measure_enter2(edit_hwnd)


        else:
            name = get_measure(edit_hwnd)

        ml = meta_dict['measures_list']
        if "[" in name and "]" in name:
            if name not in ml:
                ml.append(name)
            meta_dict['measures_list'] = ml


def input_value(value, q_list, q_dict, _key_list, text_input, q_input):
    listener.stop()
    # sleep(0.1)
    # cc1=clip.paste()
    sleep(0.1)
    clip.copy(value)
    win32api.keybd_event(8, 0, 0, 0)  # backspace
    win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    q_list.clear()
    q_dict.clear()
    key_list.clear()
    text_input = ''
    q_input.put(text_input)

    add_measure("input")  # 更新创建的度量到metadata

    # print("线程数量统计1", threading.active_count())  # 统计当前线程数量
    # print("线程list1", threading.enumerate())
    # start_listen()
    sleep(0.1)
    # clip.copy(cc1)
    t2 = threading.Thread(target=start_listen, args=(), name="key_listener")
    t2.start()

    # refresh_metadata()

    # print("线程数量统计2", threading.active_count())  # 统计当前线程数量
    # print("线程list2",threading.enumerate())


def input_text_list_sort(text_input1, meta_dict1, q_list1, q_dict1, flag):
    if flag == "table_column":
        for tc in meta_dict1['table_column_list']:

            if text_input1.lower() in tc.lower() and tc not in q_list1:
                q_list.append(tc)
    elif flag == "column":
        for c in meta_dict['column_dict'][t_name[0]]:
            if text_input1.lower() in c.lower() and c not in q_list:
                q_list.append(c)
    elif flag == "measure":
        for m in meta_dict['measures_list']:

            if text_input1.lower() in m.lower() and m not in q_list:
                q_list.append(m)
        q_list.sort()
    elif flag == "fun":
        for f in all_funs_list:
            if text_input1.lower() in f.lower() and f not in q_list:
                q_list.append(f)
        q_list.sort()
    a_list = [x for x in q_list if x[1:len(text_input1) + 1] == text_input1]
    a_list.sort()
    b_list = [x for x in q_list if x not in a_list]
    b_list.sort()
    l = a_list + b_list
    for index, iterm in enumerate(l):
        q_dict1.update({index + 1: iterm})

    return q_dict1


ud_flag = 0


def show_text_up_down(k, q_dict1):
    global ud_flag
    len_dict = len(q_dict1)
    q_dict_sp = {}
    input_text_list = []

    for t in range(len_dict // 10 + 1):
        for i in enumerate(q_dict1.items()):
            if i[0] >= (t * 10) and i[0] < (t * 10) + 10:  # 每10个元素组成一个列表
                d1 = dict([i[1]])
                q_dict_sp.update(d1)
        if q_dict_sp:
            input_text_list.append(q_dict_sp)
        q_dict_sp = {}

    len_input_text_list = len(input_text_list)

    if input_text_list:
        print("input_text_list:{}".format(input_text_list))
        if k == "Key.page_down" or k == "Key.down":
            if ud_flag == len_input_text_list - 1:
                ud_flag = len_input_text_list - 1
            else:
                ud_flag = ud_flag + 1
        elif k == "Key.page_up" or k == "Key.up":
            if ud_flag == 0:
                ud_flag = 0
            else:
                ud_flag = ud_flag - 1

        # else:
        #     ud_flag=0
        ud_dict = {}
        for i in input_text_list[ud_flag].items():
            if i[0] - 10 * ud_flag == 10:  # 10转为0
                d = {0: i[1]}
            else:
                d = {i[0] - 10 * ud_flag: i[1]}
            ud_dict.update(d)
        return ud_dict


key_list = []
q_list = []  # 输入的字符串匹配的结果列表
q_dict = {}  # q_list转为的带序号的字典，1,2,3...选择最终结果
t_name = ['']  # 用于判断是否选择表名，以供输入 '[' 显示当前表的所有列

# 监听按压

num_flag = 'n'
column_flag = 'n'
edit_hwnd = 123  #
ud_flag = 0


def close_all():
    while True:
        if not (t1.is_alive()):  # 检测gui是否退出，10秒后关闭所有线程
            os._exit(0)
        sleep(10)


def on_press(key):
    global num_flag, t_name, column_flag, edit_hwnd, thread_key_mouse_flag, edit_hwnd, input_win_title, q_list, q_dict, all_funs_list
    # print("线程数量统计00000", threading.active_count())  # 统计当前线程数量
    # print("线程list0000", threading.enumerate())
    if not (t1.is_alive()):
        os._exit(0)

    if login_flag == "yes":
        try:
            k = format(key.char)
        except:
            k = format(key)
        print(2222,k)
        if k == 'Key.f12':
            input_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            win_title_list = ["Power BI Desktop", "Tabular Editor", "记事本", "Microsoft Visual Studio", "PyCharm",
                              "DaxStudio"]
            if any(win_title_name in input_win_title for win_title_name in win_title_list):

                edit_hwnd = get_input_win()
                show_item("Binding_win")
                sleep(0.3)
                hide_item("Binding_win")
            else:
                edit_hwnd = 123
            if edit_hwnd == 123:
                hide_item('DAX Tools')
                show_item("binding_warning")
            else:
                hide_item('binding_warning')
                show_item('DAX Tools')

        if k == 'Key.space':  # 表名列名或者度量值中的名字有空格无法输入
            win_title2 = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            # print(win_title2)
            # win_title_list = ["Power BI Desktop", "Tabular Editor", \
            # "记事本", "Microsoft Visual Studio", "PyCharm","DAX Tools",]
            if "DAX Tools" in win_title2:
                set_input_win_focus(edit_hwnd)
                if key_list:
                    if key_list[0] == "'" or key_list[0] == "[" or key_list[0] == "`":
                        win32api.keybd_event(8, 0, 0, 0)  # backspace
                        win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)
            key_list.clear()
            text_input = ""
            q_input.put(text_input)
            q_dict.clear()
            q.put(q_dict)

            add_measure("space")  # 更新创建的度量到metadata

        other_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        other_handle = win32gui.FindWindow(None, other_win_title)
        daxtools_handle = win32gui.FindWindow(None, 'DAX Tools')
        if edit_hwnd == other_handle or other_handle == daxtools_handle:  # 当焦点在Tabular Editor, Power BI Desktop, VS才触发以下动作

            if k == 'Key.enter':
                add_measure("enter")

            if str(key) == "'\\x03'":  # ctrl+c 复制函数值并传递到info
                try:
                    # input_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    win_title_list = ["Power BI Desktop", "Tabular Editor", "记事本", "Microsoft Visual Studio", "PyCharm",
                                      "DaxStudio"]
                    if any(win_title_name in input_win_title for win_title_name in win_title_list):
                        clip_data = clip.paste()
                        if clip_data in all_funs_list:
                            q_cv_info.put(clip_data)
                except Exception as e:
                    print(e)

            if k != "Key.ctrl_l" and str(key) != "'\\x16'":
                if k == 'Key.esc':
                    key_list.clear()
                    text_input = ""
                    q_input.put(text_input)
                    q_dict.clear()
                    q.put(q_dict)

                if k == 'Key.backspace' and key_list:
                    if len(key_list) > 0:
                        key_list.pop()
                    if not key_list:
                        t_name = ['']
                        column_flag = 'n'

                    text_input = "".join("%s" % i for i in key_list)
                    q_input.put(text_input)
                    print('Key.backspace:', q_dict, key_list)
                    if not key_list:  # 如果key_list最后为空，返回绑定的编辑框
                        sleep(0.1)
                        set_input_win_focus(edit_hwnd)
                        # sleep(0.1)
                        win32api.keybd_event(8, 0, 0, 0)  # backspace
                        win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)

                    q.put(q_dict)

                if not (k.isdigit()):
                    q_list.clear()
                    q_dict.clear()

                if k == '/':  # 输入包含数字需要在数字前加入 /
                    num_flag = 'y'

                ##==================================================================== 表+列选择
                if k == "'":
                    key_list.clear()
                    key_list.append("'")
                    q_list.clear()
                    q_dict.clear()
                    text_input = ''
                    q_input.put(text_input)

                    sleep(0.1)
                    set_DG_focus()

                if k == "[":
                    key_list.clear()
                    key_list.append("[")
                    q_list.clear()
                    q_dict.clear()
                    text_input = ''
                    q_input.put(text_input)
                    sleep(0.1)
                    set_DG_focus()


                if "'" in key_list and num_flag == 'n' and  k != 'None' and k != '/' :
                    sleep(0.2)
                    set_DG_focus()

                    if "Key." not in k and k != "'":
                        key_list.append(k)

                    text_input = "".join("%s" % i for i in key_list[1:])
                    text_input2 = "".join("%s" % i for i in key_list)
                    q_input.put(text_input2)

                    print("表或列的文本:", text_input)

                    q_dict = input_text_list_sort(text_input, meta_dict, q_list, q_dict, "table_column")
                    print("表或列的结果字典:", q_dict)

                if "'" in key_list and k.isdigit() and num_flag == 'n' and q_dict:

                    t_name.clear()
                    tn = show_text_up_down(k, q_dict)
                    tn_len = len(tn)
                    if int(k) == 0 and tn_len == 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("表或列的最后的选择1:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    elif int(k) <= tn_len and int(k) != 0 and tn_len <= 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("表或列的最后的选择2:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    else:

                        t_name.append("{blank}")  # 为了t_name[0] 不报错



                ##=========================================================================== 列选择

                if t_name[0] in meta_dict['table_list'] and k == '[':  # 选择表后，输入'['显示当前表的所有列
                    sleep(0.1)
                    set_DG_focus()  # 焦点在DG,粘贴是需要从1开始
                    column_flag = 'y'
                    text_input2 = "".join("%s" % i for i in key_list)
                    q_input.put(text_input2)

                elif t_name[0] in meta_dict['table_list'] and k != '[' and not (k.isdigit()):  # 选择表后，输入'['显示当前表的所有列
                    column_flag = 'n'
                    t_name = ['']

                if '[' in key_list and column_flag == 'y' and k != 'None' and k != '/':
                    if "Key." not in k and k != '[':
                        key_list.append(k)
                    text_input = "".join("%s" % i for i in key_list[2:])  # 列名包含'[' 需要从第二位开始
                    text_input2 = "".join("%s" % i for i in key_list)

                    q_input.put(text_input2)
                    print("列的文本：", text_input)

                    q_dict = input_text_list_sort(text_input, meta_dict, q_list, q_dict, "column")
                    print("列的结果字典：", q_dict)

                if "[" in key_list and k.isdigit() and num_flag == 'n' and q_dict and column_flag == 'y':

                    tn = show_text_up_down(k, q_dict)
                    tn_len = len(tn)
                    if int(k) == 0 and tn_len == 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("列的最后的选择:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    elif int(k) <= tn_len and int(k) != 0 and tn_len <= 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("列的最后的选择:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    else:
                        t_name.append("{blank}")  # 为了t_name[0] 不报错

                ##================================================================================== 度量选择

                if '[' in key_list and column_flag == 'n' and k != 'None' and k != '/':

                    print("度量：", meta_dict['measures_list'])
                    sleep(0.1)
                    set_DG_focus()

                    if "Key." not in k and k != '[':
                        key_list.append(k)
                    text_input = "".join("%s" % i for i in key_list[1:])  # 度量值包含'[' 需要从第2位开始
                    text_input2 = "".join("%s" % i for i in key_list)
                    q_input.put(text_input2)
                    print("度量的文本：", text_input)


                    q_dict = input_text_list_sort(text_input, meta_dict, q_list, q_dict, "measure")
                    print("度量的结果字典：", q_dict)

                if "[" in key_list and k.isdigit() and num_flag == 'n' and q_dict and column_flag == 'n':
                    t_name.clear()
                    tn = show_text_up_down(k, q_dict)
                    tn_len = len(tn)

                    if int(k) == 0 and tn_len == 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("度量的最后的选择1:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    elif int(k) <= tn_len and int(k) != 0 and tn_len <= 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("度量的最后的选择2:", tn[int(k)])
                        input_value(tn[int(k)], q_list, q_dict, key_list, text_input, q_input)
                    else:
                        t_name.append("{blank}")  # 为了t_name[0] 不报错


                # ==========================================================================  Funs select
                if k == "`":
                    key_list.clear()
                    key_list.append("`")
                    q_list.clear()
                    q_dict.clear()
                    text_input = ''
                    q_input.put(text_input)
                    q_dict = input_text_list_sort("", meta_dict, q_list, q_dict, "fun")
                    sleep(0.1)
                    set_DG_focus()


                elif "`" in key_list and k != 'None' and k != '/' and k != "`":
                    sleep(0.1)
                    set_DG_focus()

                    if "Key." not in k and k != '`':
                        key_list.append(k)
                    text_input = "".join("%s" % i for i in key_list[1:])
                    text_input2 = "".join("%s" % i for i in key_list)
                    q_input.put(text_input2)
                    print("FUNS的文本:", text_input)
                    q_dict = input_text_list_sort(text_input, meta_dict, q_list, q_dict, "fun")
                    print("表或列的结果字典:", q_dict)

                if "`" in key_list and k.isdigit() and num_flag == 'n' and q_dict:
                    t_name.clear()
                    tn = show_text_up_down(k, q_dict)

                    tn_len = len(tn)
                    if int(k) == 0 and tn_len == 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("funs最后的选择结果1:", tn[int(k)])
                        input_value(tn[int(k)] + "(", q_list, q_dict, key_list, text_input, q_input)
                    elif int(k) <= tn_len and int(k) != 0 and tn_len <= 10:
                        set_input_win_focus(edit_hwnd)
                        t_name.append(tn[int(k)])
                        print("funs最后的选择结果2:", tn[int(k)])
                        input_value(tn[int(k)] + "(", q_list, q_dict, key_list, text_input, q_input)
                    else:
                        t_name.append("{blank}")  # 为了t_name[0] 不报错

                ##################################################################################################
                if num_flag == 'y' and k.isdigit():  # 输入包含数字的flag
                    # key_list.append(k)
                    num_flag = 'n'
                # print("t_name:", t_name)

                if q_dict:
                    r = show_text_up_down(k, q_dict)

                    if r:
                        q.put(r)
                else:
                    q.put({"blank": "yes"})


# 监听释放
def on_release(key):
    # print("已经释放:", format(key))
    # if key == Key.f12:
    #     # 停止监听
    #     return False
    None


# 开始监听
def start_listen():
    global listener
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def cb1(sender, data):
    if not (q.empty()):
        gui_q_dict = q.get()
        if "blank" in gui_q_dict:  # 判断是否不存在任何结果，返回空列表
            try:
                delete_item("Table1")
                add_table("Table1", ["_"], height=350, parent="Input", before="refresh metadate")
            except:
                None
            delete_column("Table1", 0)
            insert_column("Table1", 0, "_", [""])
        else:
            column_value = [str(k) + '. ' + v for k, v in gui_q_dict.items()]  # 展示结果
            delete_column("Table1", 0)
            insert_column("Table1", 0, "_", column_value)

            if not (gui_q_dict):
                try:
                    delete_item("Table1")
                    add_table("Table1", ["_"], height=350, parent="Input", before="refresh metadate")
                except:
                    None
                delete_column("Table1", 0)
                insert_column("Table1", 0, "_", [""])

    if not q_input.empty():
        input_text = q_input.get()

        set_value("input_text", input_text)

    # search funs action
    funs_input_text = get_value("input_funs").upper()
    if funs_input_text:
        for k, v in cate_funs.items():
            for fun in v:
                if funs_input_text not in fun:

                    hide_item(fun)
                else:
                    show_item(fun)
                if funs_input_text in fun:
                    configure_item(k, default_open=True)
    global q_cv_info, funs_detail
    if not (q_cv_info.empty()):
        funs_name = q_cv_info.get()
        funs_name = funs_name.upper()
        if funs_name in funs_detail:
            show_item("info")
            set_value("info_text", funs_detail[funs_name])
            if funs_name in shortcut_key_text_dict:
                set_value("shortcut_key_text", shortcut_key_text_dict[funs_name])
            else:
                set_value("shortcut_key_text", "")


close_expand_flag = 0


def funs_all_close_expand():
    global close_expand_flag
    if close_expand_flag == 0:
        for k, v in cate_funs.items():
            configure_item(k, label=k, parent="Funs", default_open=True, leaf=False)
        close_expand_flag = 1
    else:
        for k, v in cate_funs.items():
            configure_item(k, label=k, parent="Funs", default_open=False, leaf=False)
        close_expand_flag = 0


winTop_flag = 0


def winTop():
    sleep(0.2)
    global winTop_flag
    if winTop_flag == 0:
        hwnd = win32gui.FindWindow('DAX Tools', None)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 1300, 100, 0, 0,
                              win32con.SWP_NOSIZE)  # win32gui.SetWindowPos也可用于设置窗口大小
        winTop_flag = 1
    else:
        hwnd = win32gui.FindWindow('DAX Tools', None)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 1300, 100, 0, 0, win32con.SWP_NOSIZE)
        winTop_flag = 0


def show_funs_detail(sender, data):
    global funs_name
    funs_name = get_item_label(sender)
    show_item("info")
    set_value("info_text", funs_detail[funs_name])
    if funs_name in shortcut_key_text_dict:
        # print(shortcut_key_text_dict)
        set_value("shortcut_key_text", shortcut_key_text_dict[funs_name])
    else:
        set_value("shortcut_key_text", "")


def skip_link(sender, data):
    link = get_item_tip(sender)
    try:
        link2 = '\"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" ' + link
        os.system(link2)

    except:
        webbrowser.open(link)


def skip_link_solution(sender, data):
    link = get_item_tip(sender)
    try:
        link2 = '\"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" ' + link
        os.system(link2)
    except:
        webbrowser.open(link)


def unuseful_columns():
    global meta_dict
    unuseful_columns_list = []
    for c in meta_dict['table_column_list']:
        if c not in meta_dict['table_list']:
            for m in meta_dict['measures_list']:
                if c not in m:
                    if c not in unuseful_columns_list:
                        unuseful_columns_list.append(c)
    if not unuseful_columns_list:
        unuseful_columns_list = ["blank"]
    unuseful_columns_list.sort()

    show_item("unuseful_column_win")
    try:
        delete_item("column_group")
    except Exception as e:
        print(e)
    with group("column_group", parent="unuseful_column_win"):
        for ii in unuseful_columns_list:
            add_selectable(ii, callback=send_filter_value_to_tabular, parent="column_group")

    return unuseful_columns_list


def search_filter_var():
    global meta_dict
    search_filter_var_list = []
    for name, exp in meta_dict['measures_exp_dict'].items():
        if "filter" in exp.lower() or ("var" and "switch" in exp.lower()) or ("var" in exp.lower()):

            if name not in search_filter_var_list:
                search_filter_var_list.append(name)
    if not search_filter_var_list:
        search_filter_var_list = ["blank"]
    search_filter_var_list.sort()

    show_item("measure_win")
    try:
        delete_item("mesaure_group")
    except Exception as e:
        print(e)
    with group("mesaure_group", parent="measure_win"):
        for i in search_filter_var_list:
            add_selectable(i, callback=send_filter_value_to_tabular, parent="mesaure_group")

    return search_filter_var_list


def send_filter_value_to_tabular(sender, data):
    value = get_item_label(sender)
    if "[" in value:
        value = re.findall("\[(.*?)\]", value)[0]
    try:
        send_msg_filter(edit_hwnd, value)
    except:
        show_item("binding_warning")
    # print(value)


def clear_filter_value_to_tabular(sender, data):
    send_msg_filter(edit_hwnd, "")


def file_picker(sender, data):
    hwnd = win32gui.FindWindow('DAX Tools', None)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 1300, 100, 650, 700, win32con.SWP_SHOWWINDOW)
    sleep(0.2)
    open_file_dialog(callback=apply_selected_file, extensions=".*,.py")


login_flag = "no"
file_flag = ""


def apply_selected_file(sender, data):
    global meta_dict, login_flag, bim_path
    # configure_item("DAX Tools", width=500)
    directory = data[0]
    file = data[1]
    bim_path = directory + "\\" + file
    # with open(bim_path, 'rb') as f:
    #     data = json.load(f, strict=False)
    meta_dict = get_bim_data(bim_path)
    hide_item("Login")
    show_item('DAX Tools')
    login_flag = "yes"
    global file_flag
    file_flag = "bim"
    hwnd = win32gui.FindWindow('DAX Tools', None)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 1300, 100, 400, 650, win32con.SWP_SHOWWINDOW)
    show_item("binding_warning")


def login():
    global meta_dict, login_flag, file_flag
    databaseid = get_value("databaseid")
    localhost = get_value("localhost")
    x = 1
    try:
        meta_dict = get_meta_data(databaseid, localhost)
    except Exception as e:
        print(e)
        x = 2
    if x == 2:
        show_item("error_login")
        hide_item("Login")


    elif x == 1:
        hide_item("Login")
        show_item('DAX Tools')
        login_flag = "yes"
        file_flag = "pbix"
    set_value("input_text", "")
    set_item_label("stop input", "Input:Yes")
    show_item("binding_warning")


def refresh_metadata():
    global meta_dict, file_flag, bim_path
    databaseid = get_value("databaseid")
    localhost = get_value("localhost")
    if login_flag == "yes":
        try:
            # 更新数据
            if file_flag == "pbix":
                meta_dict = get_meta_data(databaseid, localhost)
                print("pbix", file_flag)
            elif file_flag == "bim":
                meta_dict = get_bim_data(bim_path)
                print("bim", file_flag)
            show_item("refresh_win")
            set_value("refresh_text", "    Refresh success")
            sleep(0.5)
            hide_item("refresh_win")

        except Exception as e:
            print(e)
            show_item("refresh_win")
            set_value("refresh_text", "\r\nRefresh failed\r\nPlease try again")
            sleep(1)
            hide_item("refresh_win")

    elif login_flag == "no":
        show_item("refresh_win")
        configure_item("refresh_win", width=362, x_pos=10)
        set_value("refresh_text", "\r\nRefresh failed \r\nNo [PowerBI] or [Tabular Editor] bindings")
        sleep(3)
        hide_item("refresh_win")


def login_again():
    show_item("Login")


def pbix_format_dax():
    global file_flag, bim_path
    print("pbix dax format start")
    start_time1 = time.time()
    show_item("DAX Format Warning")
    set_value("format warning", "Start DAX format,\r\nDon't do anything until it done")
    if file_flag == "pbix":
        bim_path = " "
    q_format_dax = Queue()
    gui_format_dax(file_flag, databaseid_value, localhost_value, bim_path, q_format_dax)
    print("pbix dax formatted done")
    end_time1 = time.time()
    dt = end_time1 - start_time1
    ct = "cost time:{:.0f} min {:.2f} s".format(dt // 60, dt % 60)
    print(ct)
    set_value("format warning", "DAX format done" + "\r\n" + ct)


def bim_format_dax_file_picker(sender, data):
    open_file_dialog(callback=bim_format_dax, extensions=".*,.py")


def bim_format_dax(sender, data):
    global file_flag, bim_path
    print("bim dax formatted start")
    start_time1 = time.time()
    show_item("DAX Format Warning")
    set_value("format warning", "Start DAX format,\r\nDon't do anything until it done")
    directory = data[0]
    file = data[1]
    bim_path = directory + "\\" + file
    q_format_dax = Queue()
    file_flag = "bim"
    gui_format_dax(file_flag, databaseid_value, localhost_value, bim_path, q_format_dax)
    print("bim dax formatted done")
    set_value("format warning", "DAX format done")
    end_time1 = time.time()
    dt = end_time1 - start_time1
    ct = "cost time:{:.0f} min {:.2f} s".format(dt // 60, dt % 60)
    print(ct)
    set_value("format warning", "DAX format done" + "\r\n" + ct)


def stop_key_mouse_listener():
    global thread_key_mouse_flag, q_input

    set_input_win_focus(edit_hwnd)

    if thread_key_mouse_flag == 'y':
        # print("1:",str(threading.enumerate()))
        set_item_label("stop input", "Input:No")
        set_value("input_text", "No  No  No")
        listener.stop()
        sleep(0.5)
        # print("2:",str(threading.enumerate()))
        thread_key_mouse_flag = 'n'
    elif thread_key_mouse_flag == 'n':
        t2 = threading.Thread(target=start_listen, args=(), name="key_listener")
        t2.start()
        set_item_label("stop input", "Input:Yes")
        set_value("input_text", "yes")
        thread_key_mouse_flag = 'y'


def funs_link_web_guide():
    global funs_name
    for i in all_funs_url:
        for k, v in i.items():
            if funs_name == k:
                print(v)
                link = '\"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" ' + v
                os.system(link)


def funs_link_web_micr():
    global funs_name
    micr_link1 = 'https://docs.microsoft.com/zh-cn/dax/'
    micr_link2 = micr_link1 + funs_name.lower() + '-function-dax'
    link = '\"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" ' + micr_link2
    os.system(link)


def show_shortcut_key():
    show_item("Shortcut KEY")


def show_all_on_close():
    global thread_key_mouse_flag
    show_item('DAX Tools')
    if not meta_dict:
        thread_key_mouse_flag = 'n'
        set_item_label("stop input", "Input:No")
        set_value("input_text", "No Database")


def gui(databaseid, localhost):
    try:
        # add_additional_font(r'C:\Windows\Fonts\simhei.ttf', 16, glyph_ranges='chinese_simplified_common')
        add_additional_font(r'C:\Windows\Fonts\simhei.ttf', 17, glyph_ranges='chinese_full')
    except Exception as e:
        print(e)
    with window("Login", x_pos=20, y_pos=50, width=340, height=250, on_close=show_all_on_close):
        set_main_window_title('LG1')
        set_main_window_size(600, 650)
        add_input_text("databaseid", default_value=databaseid)
        add_input_text("localhost", default_value=localhost)
        add_spacing(name="spa0", count=2, parent="Login")
        add_button("login", callback=login, parent="Login")
        add_spacing(name="spa1", count=5, parent="Login")
        add_button("select bim", callback=file_picker, parent="Login")

    with window('DAX Tools', show=False):
        set_main_window_title('DAX Tools')
        set_main_window_size(400, 650)
        with tab_bar("tbar1"):
            with tab("Input"):
                add_spacing(name="spa00", count=2, parent="Input")
                add_button(name="stop input", label="Input:Yes", callback=stop_key_mouse_listener, parent="Input")
                # set_item_color("pattern",dpg.mvGuiCol_Button, color=[51, 105, 173])
                add_same_line(spacing=190, name="sameline1", parent="Input")
                add_button("winTop", callback=winTop, width=60, label="Top", parent="Input")
                add_spacing(name="spa0", count=2, parent="Input")
                # add_input_text("input_text", default_value="", label="", parent="Input")
                add_input_text("input_text", default_value="", label="", parent="Input", readonly=True)
                add_table("Table1", ["_"], height=350, parent="Input")
                delete_column("Table1", 0)
                insert_column("Table1", 0, "_", [""])
                add_spacing(name="spa1", count=2, parent="Input")
                add_button(name="refresh metadate", label="refresh metadate",
                           tip="The Dataset had been changed ,click this button", callback=refresh_metadata,
                           parent="Input")
                add_spacing(name="spa2", count=2, parent="Input")
                add_button(name="login_again", callback=login_again, parent="Input")
                add_tab_bar(name="tab_bar1", parent="Input", show=False)
                # add_spacing(name="spa2", count=100, parent='DAX Tools')
                end()
            with tab("Funs"):
                add_input_text("input_funs", default_value="", label="Search", parent="Funs")
                add_spacing(name="spa1_Funs1", count=3, parent="Funs")
                add_button("Close or Expand ALL", callback=funs_all_close_expand)
                add_spacing(name="spa1_Funs2", count=3, parent="Funs")

                for k, v in cate_funs.items():
                    add_collapsing_header(k, label=k, parent="Funs", default_open=False)
                    for i in v:
                        add_selectable(i, callback=show_funs_detail, parent=k)
                    end()
            with tab("PBI web"):
                add_selectable(name="sqlbi",
                               tip="https://www.sqlbi.com/articles/data-model-size-with-vertipaq-analyzer/",
                               label="sqlbi", callback=skip_link)
                add_selectable(name="DAX Funs", tip="https://docs.microsoft.com/zh-cn/dax/", label="DAX Funs",
                               callback=skip_link)

                add_selectable(name="M language",
                               tip="https://docs.microsoft.com/zh-cn/powerquery-m/power-query-m-function-reference",
                               label="M language", callback=skip_link)
                add_selectable(name="DAX 权威指南中文版", tip="https://shimo.im/docs/axk6MwGPnLSpFeqr/read",
                               label="DAX 权威指南中文版",
                               callback=skip_link)

                add_selectable(name="PBI 上天", tip="https://shimo.im/docs/cyTKxj3PyhGvqxyR", label="PBI 上天",
                               callback=skip_link)
                add_selectable(name="PBI Hub", tip="https://pbihub.cn/", label="PBI Hub", callback=skip_link)

                add_selectable(name="PowerBI战友联盟", tip="https://my.oschina.net/u/4581326?tab=newest&catalogId=7034444",
                               label="PowerBI战友联盟", callback=skip_link)

                add_selectable(name="CHRIS Webb", tip="https://blog.crossjoin.co.uk/", label="CHRIS Webb",
                               callback=skip_link)
                add_selectable(name="BI Polar", tip="https://ssbipolar.com/", label="BI Polar", callback=skip_link)
                add_selectable(name="Power BI悦策", tip="https://www.zhihu.com/people/yeacer-PowerBI", label="Power BI悦策",
                               callback=skip_link)
                add_selectable(name="D-BI", tip="https://d-bi.gitee.io/", label="D-BI", callback=skip_link)
                add_selectable(name="Power Query爱好者", tip="https://pqfans.com/", label="Power Query爱好者",
                               callback=skip_link)
                add_selectable(name="Power BI极客", tip="https://www.powerbigeek.com/", label="Power BI极客",
                               callback=skip_link)
                add_selectable(name="fourmoo", tip="https://www.fourmoo.com/category/power-bi/", label="fourmoo",
                               callback=skip_link)
                add_selectable(name="Phil Seamark on DAX", tip="https://dax.tips/", label="fourmoo",
                               callback=skip_link)
                add_selectable(name="Data Veld", tip="https://dataveld.com/", label="Data Veld", callback=skip_link)
                add_selectable(name="PowerBI图表使用导航", tip="http://okviz.cn/", label="PowerBI图表使用导航", callback=skip_link)

            with tab("Solution"):
                gui_solution_dict = solution_dict
                for k, v in gui_solution_dict.items():
                    add_collapsing_header(k, label=k, parent="Solution", default_open=False)
                    for i in v:
                        # print(list(i.keys())[0])
                        add_selectable(list(i.keys())[0], callback=skip_link_solution, tip=list(i.values())[0],
                                       parent=k)
                    end()

            with tab("Optimize"):
                add_button(name="Unuseful Columns buton", label="Unrelated Columns", callback=unuseful_columns,
                           width=160, parent="Optimize")
                add_same_line(spacing=30, name="sameline2", parent="Optimize")
                add_button("Measures opt", callback=search_filter_var, width=160, parent="Optimize",
                           tip="Show Measure which has filter or var+switch")

                # add_table(name="Unuseful Column table", headers=["Unuseful Columns"], parent="Optimize", width=200,
                #           height=400)
                add_same_line(spacing=60, name="sameline3", parent="Optimize")

                add_spacing(name="spa1_Optimize1", count=110, parent="Optimize")
                add_text(name="Format ALL DAX:", parent="Optimize")
                add_spacing(name="Optimize_spa11", count=2, parent="Optimize")
                add_same_line(spacing=3, name="Optimize_line1", parent="Optimize")
                add_button("PBIX DAX", callback=pbix_format_dax, parent="Optimize")
                add_spacing(name="Optimize_spa12", count=2, parent="Optimize")
                add_same_line(spacing=3, name="Optimize_line2", parent="Optimize")
                add_button("Bim File DAX", callback=bim_format_dax_file_picker, parent="Optimize")

    with window(name="binding_warning", show=False, width=360, height=170, x_pos=10, y_pos=180):
        text = "No [PowerBI] or [Tabular Editor] bindings.\r\n1.Click on [PowerBi] or [Tabular Editor]," \
               "\r\n2.Click the [F12] to activate DAX Tools."
        text2 = "鼠标点击[ PowerBI ] or [ Tabular Editor ] \r\n再按一下[ F12 ]以绑定 DAX Tools "
        add_text(text, parent="binding_warning")
        add_spacing(name="bind_spa", count=3, parent="binding_warning")
        add_text(text2, parent="binding_warning")

    with window(name="DAX Format Warning", show=False, width=280, height=150, x_pos=100, y_pos=200):
        add_text("format warning", parent="DAX Format Warning")

    with window("info", show=False, width=360, height=290, x_pos=10, y_pos=300):
        add_text("info_text", parent="info")
        add_spacing(name="info_spa2", count=6, parent="info")
        add_same_line(spacing=2, name="info_line1", parent="info")
        add_button("DAX Guide", callback=funs_link_web_guide, parent="info")
        add_same_line(spacing=15, name="info_line2", parent="info")
        add_button("DAX zh", callback=funs_link_web_micr, parent="info")
        add_same_line(spacing=20, name="info_line0", parent="info")
        add_text("shortcut_key_text", parent="info", tip=shortcut_key_text)

    with window("measure_win", show=False, width=160, height=400, x_pos=200, y_pos=70):
        add_button(name="clear1", label="clear", callback=clear_filter_value_to_tabular)
        with group("mesaure_group", parent="measure_win"):
            add_text("__")

    with window("unuseful_column_win", show=False, width=160, height=400, x_pos=10, y_pos=70):
        add_button(name="clear2", label="clear", callback=clear_filter_value_to_tabular)
        with group("column_group", parent="unuseful_column_win"):
            add_text("___")

    with window("Shortcut KEY", width=340, height=265, x_pos=80, y_pos=200, show=False):
        add_text(shortcut_key_text)

    with window("error_login", x_pos=20, y_pos=70, width=330, height=160, show=False):
        text3 = "Wrong databaseID or localhost value"
        add_text(text3, parent="error_login")

    with window("Binding_win", x_pos=80, y_pos=350, width=250, height=150, show=False):
        text4 = "    Binding success"
        add_text(name="text4", default_value=text4, parent="Binding_win")
        add_spacing(name="Binding_win_spa", count=6, parent="Binding_win")
        text5 = "        绑定成功"
        add_text(name="text5", default_value=text5, parent="Binding_win")

    with window("refresh_win", x_pos=80, y_pos=300, width=250, height=150, show=False):
        add_text(name="refresh_text", default_value="   Refresh success", parent="refresh_win")

    set_render_callback(cb1)
    start_dearpygui(primary_window='DAX Tools')


def destory_waring_win():
    sleep(1)
    # exit()
    os._exit(0)


def warning_win():
    with window("warning!", x_pos=10, y_pos=10):
        try:
            add_additional_font(r'C:\Windows\Fonts\simhei.ttf', 17, glyph_ranges='chinese_simplified_common')
        except Exception as e:
            print(e)
        set_main_window_title('warning!')
        set_main_window_size(260, 280)
        add_text("Another program,\r\ncalled Dax Tools,\r\nis already running")
    set_render_callback(destory_waring_win)
    start_dearpygui()


if __name__ == '__main__':
    win_title = get_all_win_title()

    if "DAX Tools" in win_title:
        warning_win()

    try:
        databaseid_value = sys.argv[2]
        localhost_value = sys.argv[1]
    except:
        databaseid_value = ""
        localhost_value = ""
        # databaseid_value = "a2d7001e-e236-4c81-89be-d5efc95bf6fc"
        # localhost_value = "localhost:63508"

    q_funs_data = Queue()
    meta_dict = {}
    funs_data = funs_data_list  # funs_data_list.py
    cate_funs = funs_data[1]
    funs_detail = funs_data[0]
    all_funs_list = [x for i in list(cate_funs.values()) for x in i]
    all_funs_url = funs_data[2]

    thread_list = []
    t1 = threading.Thread(target=gui, args=(databaseid_value, localhost_value), name="gui")
    t2 = threading.Thread(target=start_listen, args=(), name="key_listener")
    t3 = threading.Thread(target=winTop, args=(), name="wintop")
    t4 = threading.Thread(target=funs_combkey_listener, args=(), name="combkey_listener")
    t5 = threading.Thread(target=close_all, args=(), name="close")
    # t6 = threading.Thread(target=daxformat_main, args=(), name="daxformat_main")

    thread_list = [t1, t2, t3, t4, t5]
    for t in thread_list:
        t.start()
