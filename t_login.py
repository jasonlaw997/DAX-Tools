from dearpygui.core import *
from dearpygui.simple import *
import json
with open('funs.json', 'rb') as f:
    data = json.load(f,strict=False)

def hide_lg():
    print(222)
    # hide_item("Login")

def file_picker(sender, data):
    open_file_dialog(callback=apply_selected_file, extensions=".*,.py")

def apply_selected_file(sender, data):
    directory = data[0]
    file = data[1]
    bim_path=directory+"\\"+file
    with open(bim_path, 'rb') as f:
        data = json.load(f, strict=False)
    hide_item("Login")


def login_window():

    with window("Login",x_pos=40,y_pos=50,width=280,height=250):
        set_main_window_title('LG1')
        set_main_window_size(600, 650)
        add_additional_font(r'C:\Windows\Fonts\simhei.ttf', 16, glyph_ranges='chinese_simplified_common')
        add_input_text("databaseid")
        add_input_text("localhost")
        add_button("login",callback=hide_lg)
        add_button("select bim",callback=file_picker)
    start_dearpygui()

if __name__ == '__main__':
    login_window()