import tkinter


def simple_tkinter_dialog(dic):
    for keys in dic.keys():
        dic[keys] = tkinter.simpledialog.askinteger("", keys)
    return dic