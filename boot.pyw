# -*- coding: ascii -*-
"""
this is the boot unity of the datanalyze environment
for running the app, this part is required during the booting process.
No models or function could run without the booting process.

author: Wang Weizheng
build time: 06/14/2019 22:59

Copyright (C) 2019 Weizheng Wang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


if __name__ != '__main__':
    raise ImportError("this module could not be imported!")

import sys
import os
from typing import Any, Union, TextIO, Type
from config.config_library import set_config, save_config, printf


INIT_IMPORT_LIST = []


def set_screen_zoom(raw_magnify_ratio: float) -> None:
    """
setting the windows zoom ratio. 
    """
    if get_config("$default_GUI_force_set_zoom_ratio") is not None:
        set_config("dpi_scale", get_config("$default_GUI_force_set_zoom_ratio"))
        wx.MessageBox(f"the DPI scale has been sat manually to {get_config('dpi_scale')}.")

    dpi_scale: float = raw_magnify_ratio * get_config("$default_GUI_force_set_zoom_bias_multiply") + get_config(
        "$default_GUI_force_set_zoom_bias_add")  # UI magnify ratio
    set_config(dpi_scale=dpi_scale)


def set_display_magnify_and_config() -> float:
    # detect vertical screen
    scr_logic_x: int = GetSystemMetrics(0); scr_logic_y: int = GetSystemMetrics(1)
    set_config(is_vertical_screen=scr_logic_x < scr_logic_y)

    #  set the display resolution magnify ratio.
    ctypes.windll.shcore.SetProcessDpiAwareness(get_config("$default_GUI_os_process_dpi_awareness"))

    return GetSystemMetrics(0) / scr_logic_x  # the screen original magnify ratio


def get_import_list() -> list:
    try:
        import_list_file: TextIO = open(r"config\import list.cfg", 'r')
    except IOError or WindowsError or FileNotFoundError:
        set_import_list()
        import_list_file: TextIO = open(r"config\import list.cfg", 'r')
    import_list: dict = eval(import_list_file.read())
    import_list_file.close()
    return import_list


def set_import_list():
    try:
        import_list_file: TextIO = open(r"config\import list.cfg", 'w')
    except IOError or WindowsError or FileNotFoundError:
        raise EnvInitFail(set_import_list, message=r"failed to load booting behavior, please check the "
                                                   r"config\import list.cfg file.")
    import_list_file.write("#please list the file which you want to import during the loading progress. \n#it "
                           "is not recommend to change this file unless you could make sure these models will work in "
                           "the datanalysis environment.\n")
    import_list_file.write(str(INIT_IMPORT_LIST))
    # these are basic lib for math and data analyze.
    import_list_file.close()


def check_imports():
    for curr_import in get_import_list():
        try:
            __import__(curr_import)
        except Exception as ERROR:
            wx.MessageBox(f"failed to load {curr_import} model, the program could not execute. {ERROR}")


if __name__ == "__main__":

    try:
        from config.config_library import get_config, set_config, EnvInitFail, save_config, RaisedExit
    except ImportError as e:
        raise BaseException(f"failed to load config, the program could not execute. {e}")

    try:
        import wx
        from wx import Frame, App, Font, TextCtrl
    except ImportError:
        set_config(ui_boot_fail=True)
        save_config()
        printf("boot failed, failed to import Wxpython framework.")
        sys.exit(1)
    else:
        app: App = wx.App()

    try:
        # noinspection PyUnresolvedReferences
        from win32api import GetSystemMetrics
        # noinspection PyUnresolvedReferences
        import ctypes
        raw_magnify_ratio = set_display_magnify_and_config()
    except ImportError:
        raw_magnify_ratio = 1
        wx.MessageBox(r'failed to import windows32 API lib. This may due to operating system type. Only windows is '
                      r'recommended for running this software smoothly, and the support for other platform is still '
                      r'developing and unstable. If you are using windows, please make sure to use the interpreter '
                      r'which installed win32 lib.')

    set_screen_zoom(raw_magnify_ratio)

    dpi = get_config("dpi_scale")

    wf: Type[Frame] = wx.Frame
    frame: Frame = wf(None, title="", size=(int(500 * dpi), int(80 * dpi)), style=1)
    frame.SetTransparent(200)
    frame.SetMaxSize((int(500 * dpi), int(80 * dpi)))
    frame.SetMinSize((int(500 * dpi), int(80 * dpi)))
    font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Microsoft YaHei")
    wf.box = wx.TextCtrl(frame, pos=(-2, int(50*dpi)), size=(int(504 * dpi), int(30 * dpi)), style=wx.TE_CENTER)
    wf.box.SetFont(font)
    wf.box.AppendText("Loading")
    wf.box.SetCanFocus(False)

    frame.Center()
    frame.Show()
    check_imports()
    frame.Destroy()

    save_config()

    try:
        import config.run
    except SystemExit:
        sys.exit()
    except RaisedExit:
        sys.exit()
    except Exception as e:
        save_config()
        wx.MessageBox(f"I'm sorry. A fatal error occurred in the execution of the program. Your configurations have "
                      "been saved. \n {e}")
