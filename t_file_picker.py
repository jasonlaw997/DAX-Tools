from dearpygui.core import *
from dearpygui.simple import *
import json
# with open('funs.json', 'rb') as f:
#     data = json.load(f,strict=False)


add_additional_font(r'C:\Windows\Fonts\simhei.ttf', 16, glyph_ranges='chinese_simplified_common')

def file_picker(sender, data):
    open_file_dialog(callback=apply_selected_file, extensions=".*,.py")

def apply_selected_file(sender, data):
    log_debug(data)
    directory = data[0]
    file = data[1]
    set_value("目录", directory)
    set_value("文件", file)
    set_value("文件路径", f"{directory}\\{file}")
    bim_path=directory+"\\"+file
    with open(bim_path, 'rb') as f:
        data = json.load(f, strict=False)
    print(data)
show_logger()

with window("Tutorial"):
    add_button("文件选择器", callback=file_picker)
    add_text("目录路径: ")
    add_same_line()
    add_label_text("##filedir", source="目录", color=[255, 0, 0])
    add_text("文件: ")
    add_same_line()
    add_label_text("##file", source="文件", color=[255, 0, 0])
    add_text("文件路径: ")
    add_same_line()
    add_label_text("##filepath", source="文件路径", color=[255, 0, 0])

start_dearpygui()