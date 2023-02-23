import PySimpleGUI as sg
from change import ChangeFile
import json


layout = [[sg.Text('请选择一个文件', size=(8, 2))],
          [sg.Text('类型名称', size=(8, 2)), sg.DropDown(
              ['cs', 'cpp', 'python', 'java', 'sh', 'js'], default_value='cs', key='keyword')],
          [sg.Text('路径', size=(8, 2)), sg.Input('', key='ref'),
           sg.FilesBrowse(initial_folder="./", file_types=[("*", "md")])],
          [sg.OK(), sg.Quit()]]

# 创建窗口并显示
window = sg.Window('选择文件', layout)
while(True):
    event, values = window.read()
    # 处理事件和输入值
    if event == 'OK':
        error_msgs = []
        file_paths = values["ref"].split(';')
        keyword = values['keyword']
        for file_path in file_paths:
            cf = ChangeFile(file_path, keyword)
            res = cf.dochange()
            if res != True:
                error_msgs.append(
                    f"{file_path}修改失败\n异常类型：{type(res)}\n错误内容：{res.args}")
        if len(error_msgs) > 0:
            err_msg = ""
            for msg in error_msgs:
                err_msg += f"error{error_msgs.index(msg)+1}\n"
                err_msg += msg
                err_msg += "\n\n"
            sg.popup(err_msg)
        else:
            sg.popup('修改成功', title='修改成功')

    elif event == sg.WIN_CLOSED or event == 'Quit':
        break

# 关闭窗口
window.close()
