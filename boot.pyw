# -*- coding: ascii -*-
"""
this is the boot unity of the datanalyze environment
for running the app, this part is required during the booting process.
No modules or function could run without the booting process.

author: Wang Weizheng
build time: 06/14/2019 22:59

COPYRIGHT INFORMATION:

Copyleft (C) 2020  Weizheng Wang
this software is licensed under Unlicense license

This is free and unencumbered software released into the public domain.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

import sys

from typing import Any, Union, TextIO, Type, List
from config.config_library import fprintf

INIT_CUSTOM_IMPORT_LIST = []

INIT_PROJECT_IMPORT_LIST = ['Angelina']


def set_screen_zoom(raw_magnify_ratio: float) -> None:
    """
setting the windows zoom ratio. 
    """
    if get_config("GUI_force_set_zoom_ratio") is not None:
        set_config("dpi_scale", get_config("GUI_force_set_zoom_ratio"))
        wx.MessageBox(f"the DPI scale has been sat manually to {get_config('dpi_scale')}.")

    dpi_scale: float = raw_magnify_ratio * get_config("GUI_force_set_zoom_bias_multiply") + get_config(
        "GUI_force_set_zoom_bias_add")  # UI magnify ratio
    set_config(dpi_scale=dpi_scale)


def set_display_magnify_and_config() -> float:
    # detect vertical screen
    scr_logic_x: int = GetSystemMetrics(0);
    scr_logic_y: int = GetSystemMetrics(1)
    set_config(is_vertical_screen=scr_logic_x < scr_logic_y)

    #  set the display resolution magnify ratio.
    ctypes.windll.shcore.SetProcessDpiAwareness(get_config("GUI_os_process_dpi_awareness"))

    return GetSystemMetrics(0) / scr_logic_x  # the screen original magnify ratio


def get_import_list() -> List[str]:
    try:
        import_list_file: TextIO = open(r"config\import list.cfg", 'r')
    except IOError or WindowsError or FileNotFoundError:
        set_import_list()
        import_list_file: TextIO = open(r"config\import list.cfg", 'r')
    import_list: List[str] = import_list_file.read().split('\n')
    import_list_file.close()
    return import_list


def set_import_list():
    try:
        import_list_file: TextIO = open(r"config\import list.cfg", 'w')
    except IOError or WindowsError or FileNotFoundError:
        raise EnvInitFail(set_import_list, message=r"failed to load booting behavior, please check the "
                                                   r"config\import list.cfg file.")
    import_list_file.write('\n'.join(INIT_CUSTOM_IMPORT_LIST))
    # these are basic lib for math and data analyze.
    import_list_file.close()


def check_imports():
    full_module_name: list = INIT_PROJECT_IMPORT_LIST + (_ := get_import_list())
    full_module_list: list = INIT_PROJECT_IMPORT_LIST + ["Lib." + _ for _ in _]
    for index, curr_import in enumerate(full_module_list):
        if not curr_import == 'Lib.':
            try:
                exec(f"{full_module_name[index]} = __import__('{curr_import}')")
            except Exception as ERROR:
                wx.MessageBox(f"failed to load {curr_import} module, the program may occurs errors. {ERROR}")


if __name__ == "__main__":

    try:
        from config.config_library import get_config, set_config, EnvInitFail, save_config, RaisedExit
    except ImportError as e:
        raise BaseException(f"failed to load config, the program could not execute. {e}")

    try:
        import wx
        from wx import Frame, App, Font, TextCtrl
    except ImportError:
        fprintf("boot failed, failed to import Wxpython framework.")
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
    wf.box = wx.TextCtrl(frame, pos=(-2, int(50 * dpi)), size=(int(504 * dpi), int(30 * dpi)), style=wx.TE_CENTER)
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
