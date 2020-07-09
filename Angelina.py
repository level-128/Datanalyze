"""
this is the main GUI interface of the program.

author: Weizheng Wang
build time: 11/9/2019 19:45

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

import os
import sys
import time
# noinspection PyUnresolvedReferences
from math import *  # DO NOT DELETE THIS

import wx

import Benjamin
import David
from config.config_library import get_config, set_config, save_config, clear_vars, debug_log, fprintf

HELP_WEBSITE = 'https://github.com/EPIC-WANG/Datanalyze'  # the website if user tapped HELP


# noinspection DuplicatedCode,PyAttributeOutsideInit
# the GUI contains too many duplicated codes, and you know why.
# noinspection PyUnusedLocal
class Alexander(wx.Frame):
    dpi = get_config("dpi_scale", 1.0)
    INIT_WINDOW_SIZE_HOR: tuple = (420 * dpi, 320 * dpi)
    INIT_WINDOW_SIZE_VER: tuple = (420 * dpi, 320 * dpi)
    FULL_WINDOW_SIZE_HOR: tuple = (850 * dpi, 372 * dpi)
    FULL_WINDOW_SIZE_VER: tuple = (460 * dpi, 830 * dpi)
    MIN_WINDOW_SIZE_HOR: tuple = (420 * dpi, 170 * dpi)
    MIN_WINDOW_SIZE_VER: tuple = (420 * dpi, 170 * dpi)
    MAX_CHOICE_SIZE: tuple = (-1, 36 * dpi)

    @debug_log
    def __init__(self) -> None:

        self.hbox_1_l3_comp = None
        self.hbox_1_l2_comp = None
        self.hbox_1_l1_2_comp = None
        self.hbox_1_l1_1_comp = None
        self.winfont = None
        self.font_tc_equ = None
        self.panel = None

        # noinspection PyUnresolvedReferences
        def set_font():
            self.font_tc_equ = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Consolas")
            self.winfont = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Segoe UI")

        @debug_log
        def set_menu_bar():
            menu_bar = wx.MenuBar()

            appmenu = wx.Menu()
            menu_bar.Append(appmenu, "&Program")
            menu_close = appmenu.Append(wx.ID_ANY, "Exit")
            menu_settings = appmenu.Append(wx.ID_ANY, "Settings")
            menu_abort = appmenu.Append(wx.ID_ANY, "Abort the program")
            self.Bind(wx.EVT_MENU, self.on_close, menu_close)
            self.Bind(wx.EVT_MENU, self.on_settings, menu_settings)
            self.Bind(wx.EVT_MENU, self.on_abort, menu_abort)

            plotfilemenu = wx.Menu()
            menu_bar.Append(plotfilemenu, "&File")
            menu_save_figure = plotfilemenu.Append(wx.ID_ANY, "Quick save last figure")
            menu_save_config = plotfilemenu.Append(wx.ID_ANY, "Save config")
            menu_display_config = plotfilemenu.Append(wx.ID_ANY, "Display config")
            self.Bind(wx.EVT_MENU, self.on_save_figure, menu_save_figure)
            self.Bind(wx.EVT_MENU, self.on_save_config, menu_save_config)
            self.Bind(wx.EVT_MENU, self.on_display_config, menu_display_config)

            advancedmenu = wx.Menu()
            menu_bar.Append(advancedmenu, "&Advanced")
            menu_reset_config = advancedmenu.Append(wx.ID_ANY, "Reset config")
            menu_clear_config = advancedmenu.Append(wx.ID_ANY, "Clear config")
            self.Bind(wx.EVT_MENU, self.on_clear_config, menu_clear_config)
            self.Bind(wx.EVT_MENU, self.on_reset_config, menu_reset_config)

            helpmenu = wx.Menu()
            menu_bar.Append(helpmenu, "&Help")
            menu_tutorial = helpmenu.Append(wx.ID_ANY, "Tutorial")
            menu_about = helpmenu.Append(wx.ID_ANY, "About")
            self.Bind(wx.EVT_MENU, self.on_tutorial, menu_tutorial)
            self.Bind(wx.EVT_MENU, self.on_about, menu_about)

            self.SetMenuBar(menu_bar)

        # noinspection PyAttributeOutsideInit
        @debug_log
        def set_panel():
            self.panel = wx.Panel(parent=self)
            __panel_hbox_1_l1()
            __panel_hbox_1_l2()
            hbox_1_l3()
            box_comp_main()
            self.trig_show_basic_opt()

        def __panel_hbox_1_l1():
            panel, dpi = self.panel, self.dpi
            self.create_new_fig = wx.Button(panel, label='start new', size=(110 * dpi, 60 * dpi))
            self.create_new_fig.Bind(wx.EVT_BUTTON, self.on_create_new_fig)
            self.start_plot_btn = wx.Button(panel, label='continue', size=(110 * dpi, 60 * dpi))
            self.start_plot_btn.Bind(wx.EVT_BUTTON, self.on_start_plot_button)
            self.settings_btn = wx.Button(panel, label='settings', size=(110 * dpi, 60 * dpi))
            self.settings_btn.Bind(wx.EVT_BUTTON, self.on_settings)

            self.input_syntax = wx.CheckBox(panel, label="python mode")
            # self.is_python_input = wx.CheckBox(panel, -1, "input the python command")

            self.is_advanced_mode = wx.CheckBox(panel, label="advanced mode")
            self.is_advanced_mode.Bind(wx.EVT_LEFT_DOWN, self.on_advanced_mode)
            self.is_advanced_mode.SetValue(get_config('is_advanced_mode'))

            self.tc_equ = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, size=(280 * dpi, -1))
            self.tc_equ.AppendText('please input your math equation or commands in here.')

            self.tc_equ.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self.on_tc_equ_left_down)

            hbox0_2 = wx.BoxSizer(wx.VERTICAL)
            hbox0_2.Add(self.create_new_fig, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)
            hbox0_2.Add(self.start_plot_btn, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)
            hbox0_2.Add(self.settings_btn, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)
            hbox0_2.Add(self.is_advanced_mode, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)
            hbox0_2.Add(self.input_syntax, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)

            self.tc_equ.SetFont(self.font_tc_equ)
            self.create_new_fig.SetFont(self.winfont)
            self.start_plot_btn.SetFont(self.winfont)
            self.settings_btn.SetFont(self.winfont)
            self.input_syntax.SetFont(self.winfont)
            self.is_advanced_mode.SetFont(self.winfont)
            self.hbox_1_l1_1_comp = self.tc_equ
            self.hbox_1_l1_2_comp = hbox0_2

        def __panel_hbox_1_l2():
            panel, dpi = self.panel, self.dpi
            statictext3_1 = wx.StaticText(panel, label="Left X axis", size=(-1, 20 * self.dpi))
            statictext3_2 = wx.StaticText(panel, label="Right X axis", size=(-1, 20 * self.dpi))
            self.input9_xllim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            self.input10_xrlim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            statictext3_3 = wx.StaticText(panel, label="Left Y axis", size=(-1, 20 * self.dpi))
            statictext3_4 = wx.StaticText(panel, label="Right Y axis", size=(-1, 20 * self.dpi))
            self.input11_yllim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            self.input12_yrlim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            statictext3_5 = wx.StaticText(panel, label="Left Z axis", size=(-1, 20 * self.dpi))
            statictext3_6 = wx.StaticText(panel, label="Right Z axis", size=(-1, 20 * self.dpi))
            self.input24_3d_zllim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            self.input25_3d_zrlim = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))

            hbox_t6 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t6.Add(statictext3_1, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t6.Add(statictext3_2, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            hbox_t7 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t7.Add(self.input9_xllim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t7.Add(self.input10_xrlim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            hbox_t8 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t8.Add(statictext3_3, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t8.Add(statictext3_4, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            hbox_t9 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t9.Add(self.input11_yllim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t9.Add(self.input12_yrlim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            hbox_t10 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t10.Add(statictext3_5, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t10.Add(statictext3_6, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            hbox_t11 = wx.BoxSizer(wx.HORIZONTAL)
            hbox_t11.Add(self.input24_3d_zllim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)
            hbox_t11.Add(self.input25_3d_zrlim, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=4 * dpi)

            statictext3_8 = wx.StaticText(panel, label="plotting accurcy")

            self.calc_count = wx.TextCtrl(panel, -1, size=(-1, 24 * self.dpi))
            self.calc_count.SetValue("500")
            self.calc_count.Enable(get_config('is_advanced_mode'))
            self.calc_count.SetMaxSize(self.MAX_CHOICE_SIZE)
            self.other_plot_acc = self.calc_count  # for capability

            statictext3_9 = wx.StaticText(panel, label='plotting mode')

            self.figspine = wx.ComboBox(panel, -1, choices=['normal', 'coord', 'L', 'sign'])
            self.figspine.SetValue(get_config('figspine'))
            self.figspine.Enable(get_config('is_advanced_mode'))
            self.figspine.SetMaxSize(self.MAX_CHOICE_SIZE)

            for _ in (
                    'statictext3_1', 'statictext3_2', 'statictext3_3', 'statictext3_4', 'statictext3_5',
                    'statictext3_6', 'statictext3_8', 'statictext3_9', 'self.input9_xllim', 'self.input10_xrlim',
                    'self.input11_yllim', 'self.input12_yrlim', 'self.input24_3d_zllim', 'self.input25_3d_zrlim',
                    'self.calc_count', 'self.figspine'):
                eval(_).SetFont(self.winfont)

            vbox2_0 = wx.BoxSizer(wx.VERTICAL)
            for _ in [hbox_t6, hbox_t7, hbox_t8, hbox_t9, hbox_t10, hbox_t11]:
                vbox2_0.Add(_, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
            for _ in [statictext3_8, self.calc_count, statictext3_9, self.figspine]:
                vbox2_0.Add(_, 1, flag=wx.ALL | wx.EXPAND, border=4 * dpi)
            self.hbox_1_l2_comp = vbox2_0

        # noinspection PyAttributeOutsideInit
        def hbox_1_l3():
            panel, dpi = self.panel, self.dpi
            statictext2_4 = wx.StaticText(panel, label='choose colour:\nPress Ctrl or shift to muti-choice',
                                          style=wx.TE_LEFT)
            self.colour_opt = ["black", "red", "blue", "green", "yellow",
                               "orange", "brown", "purple", "cyan", "light blue"]
            self.colourbox = wx.ListBox(panel, -1, choices=self.colour_opt, style=wx.LB_EXTENDED)

            statictext1_4 = wx.StaticText(panel, label='choose line pattern:')
            self.cho5_linestyle = wx.ComboBox(panel, -1, choices=["solid", "dotted", "dashed", "dashdot"])
            self.cho5_linestyle.SetValue("solid")
            self.cho5_linestyle.Enable(get_config('is_advanced_mode'))
            self.cho5_linestyle.SetMaxSize(self.MAX_CHOICE_SIZE)

            vbox2_0 = wx.BoxSizer(wx.VERTICAL)
            vbox2_0.Add(statictext2_4, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
            vbox2_0.Add(self.colourbox, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
            vbox2_0.Add(statictext1_4, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
            vbox2_0.Add(self.cho5_linestyle, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)

            statictext2_4.SetFont(self.winfont)
            self.colourbox.SetFont(self.winfont)
            statictext1_4.SetFont(self.winfont)
            self.cho5_linestyle.SetFont(self.winfont)

            self.hbox_1_l3_comp = vbox2_0

        def box_comp_main():
            dpi = self.dpi
            if get_config('is_vertical_screen', False):
                self.SetMinSize(self.MIN_WINDOW_SIZE_VER)
                hbox_main_1 = wx.BoxSizer(wx.HORIZONTAL)
                hbox_main_2 = wx.BoxSizer(wx.HORIZONTAL)
                hbox_main_1.Add(self.hbox_1_l1_1_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main_1.Add(self.hbox_1_l1_2_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main_2.Add(self.hbox_1_l2_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main_2.Add(self.hbox_1_l3_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main = wx.BoxSizer(wx.VERTICAL)
                hbox_main.Add(hbox_main_1, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main.Add(hbox_main_2, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                self.panel.SetSizer(hbox_main)
            else:
                self.SetMinSize(self.MIN_WINDOW_SIZE_HOR)
                hbox_main = wx.BoxSizer(wx.HORIZONTAL)
                hbox_main.Add(self.hbox_1_l1_1_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main.Add(self.hbox_1_l1_2_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main.Add(self.hbox_1_l2_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                hbox_main.Add(self.hbox_1_l3_comp, 1, flag=wx.ALL | wx.EXPAND, border=2 * dpi)
                self.panel.SetSizer(hbox_main)

        self.frame = wx.Frame.__init__(self, parent=None, title="Main Frame")
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Center()

        set_font()
        set_menu_bar()
        set_panel()

    """
    Events:
    """

    @debug_log
    def on_close(self, event=None):
        dlg = wx.MessageDialog(self.panel, "Do You Want to save your last plotting configuration and Exit?", "Exit",
                               style=wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT)
        option = dlg.ShowModal()
        if option == wx.ID_CANCEL:
            return None
        if option == wx.ID_YES:
            save_config()
        sys.exit(0)

    @debug_log
    def on_clear_config(self, event=None):
        dlg = wx.MessageDialog(self.panel, "Do You Want to clear the user variables?", "reset",
                               style=wx.YES_NO | wx.NO_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            clear_vars(save=True)
            wx.MessageBox("Done")

    @staticmethod
    def on_save_config(event=None):
        save_config()
        wx.MessageBox("Done")

    @staticmethod
    @debug_log
    def on_display_config(event=None):
        os.startfile(r"config\bootconfig.cfg")

    @staticmethod
    @debug_log
    def on_about(event=None):
        wx.MessageBox(f"""Datanalyze version {get_config('version')}

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

to view GitHub Project page, visit:
https://github.com/EPIC-WANG/PythonLinearAlgebra
""")

    @staticmethod
    @debug_log
    def on_abort(event=None):
        os.abort()

    @staticmethod
    def on_settings(event=None):
        settings_frame = David.Donald()
        settings_frame.Show()

    @debug_log
    def trig_set_basic_opt(self):
        """
        set the value of the
        """
        colour_list = [self.colour_opt[selected_colour] for selected_colour in self.colourbox.GetSelections()]
        set_config(colour=colour_list if colour_list else ['black'])
        set_config(xllim=eval(self.input9_xllim.GetValue()),
                   xrlim=eval(self.input10_xrlim.GetValue()),
                   yllim=eval(self.input11_yllim.GetValue()),
                   yrlim=eval(self.input12_yrlim.GetValue()),
                   zllim=eval(self.input24_3d_zllim.GetValue()),
                   zrlim=eval(self.input25_3d_zrlim.GetValue()),
                   calc_count=int(self.calc_count.GetValue()),
                   figspine=self.figspine.GetValue(),
                   linestyle=self.cho5_linestyle.GetValue())

    def trig_show_basic_opt(self):
        self.input9_xllim.SetValue(str(get_config('xllim', -5)))
        self.input10_xrlim.SetValue(str(get_config('xrlim', 5)))
        self.input11_yllim.SetValue(str(get_config('yllim', -5)))
        self.input12_yrlim.SetValue(str(get_config('yrlim', 5)))
        self.input24_3d_zllim.SetValue(str(get_config('zllim', -5)))
        self.input25_3d_zrlim.SetValue(str(get_config('zrlim', 5)))

    def __is_runable(self) -> bool:
        return bool(self.tc_equ.GetValue().replace('please input your math equation or commands in here.', '')
                    .replace('\n', '').lstrip())

    @debug_log
    def start_plot_button(self, new_fig: bool):
        if not self.__is_runable():
            wx.MessageBox("please input your math equation or commands in the box!")
            return None

        try:
            self.trig_set_basic_opt()
        except SyntaxError:
            wx.MessageBox("Please check the syntax of the expression in domain/range settings. Only Python syntax could"
                          " be input in the box.")
            return None
        except Exception as _:
            wx.MessageBox(f"A error occurs when trying to interpret the expression in domain/range settings: {_}")
            return None

        inputed_function: str = self.tc_equ.GetValue()

        fprintf(f"python_mode = {(python_mode := self.input_syntax.GetValue())}", self_=self.start_plot_button)

        if inputed_function != '':
            current_line = 'unknown'
            function = 'unknown'
            try:  # TODO: move these
                if python_mode is False:  # it is none python mode
                    current_line = 1
                    function: str  # the input equation in each line
                    for function in inputed_function.split('\n'):
                        if not function.isspace() and function != '':
                            fprintf(f"{function=}", self_=self.start_plot_button)
                            Benjamin.plot(function, False, new_fig)
                            new_fig = False
                        current_line += 1

                else:
                    fprintf(f"{inputed_function=}", self_=self.start_plot_button)
                    Benjamin.plot(inputed_function, True, new_fig)
                    wx.MessageBox("Done!")

            except KeyboardInterrupt:
                fprintf(f"User has canceled the operation in line {current_line}", self_=self.start_plot_button)
                wx.MessageBox(f"User has canceled the operation in line {current_line}")
            except Exception as _:
                fprintf(f"A error occurs during the executing progress in line {current_line}: '{function}': {str(_)}",
                        self_=self.start_plot_button)
                wx.MessageBox(
                    f"A error occurs during the executing progress in line {current_line}: '{function}' \n {str(_)}")
            Benjamin.show()
        return None

    def on_tc_equ_left_down(self, event=None):
        if self.tc_equ.GetValue() == 'please input your math equation or commands in here.':
            self.tc_equ.Clear()

    def on_create_new_fig(self, event=None):
        self.start_plot_button(True)

    def on_start_plot_button(self, event=None):
        self.start_plot_button(False)

    @debug_log
    def __toggle_advanced_config(self, is_advanced_mode: bool):
        if not is_advanced_mode:
            # set the value to the default
            self.calc_count.SetValue(str(get_config("calc_count")))
            self.figspine.SetValue(get_config("figspine"))
            self.cho5_linestyle.SetValue(get_config("linestyle"))

        self.calc_count.Enable(is_advanced_mode)
        self.figspine.Enable(is_advanced_mode)
        self.cho5_linestyle.Enable(is_advanced_mode)

    @debug_log
    def on_advanced_mode(self, event=None):
        is_advanced_mode: bool = not self.is_advanced_mode.GetValue()
        self.is_advanced_mode.SetValue(is_advanced_mode)
        set_config(advanced_mode=is_advanced_mode)
        window_size: tuple = self.GetSize()
        if is_advanced_mode and window_size[0] <= 575 * self.dpi and window_size[1] <= 400 * self.dpi:
            if get_config("is_vertical_screen"):
                self.SetSize(self.FULL_WINDOW_SIZE_VER)
            else:
                self.SetSize(self.FULL_WINDOW_SIZE_HOR)
        self.__toggle_advanced_config(is_advanced_mode)
        if is_advanced_mode:
            time.sleep(0.4)

    @debug_log
    def on_reset_config(self, event=None):
        dlg = wx.MessageDialog(self.panel,
                               "Do You Want to reset and close the program? this will fix the issue of the program.",
                               "reset",
                               style=wx.YES_NO | wx.NO_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            os.remove(r"config\bootconfig.cfg")
            python = sys.executable
            os.execl(python, python, *sys.argv)

    @staticmethod
    @debug_log
    def on_save_figure(event=None):
        if not Benjamin.current_plt:  # the figure does not exist
            wx.MessageBox("save figure failed, you haven't plot any figure yet.")
            return
        try:
            wx.MessageBox(f"save figure '{Benjamin.save()}' successful.")
        except Exception as _:
            wx.MessageBox(f"save figure failed, {_}")

    @staticmethod
    @debug_log
    def on_tutorial(event=None):
        import webbrowser
        webbrowser.open(HELP_WEBSITE)
        wx.MessageBox("tutorial has opened in your web browser.")


class Alex(wx.App):

    @debug_log
    def OnInit(self):
        frame = Alexander()
        if get_config("is_vertical_screen"):
            frame.SetSize(frame.FULL_WINDOW_SIZE_VER if get_config("is_advanced_mode") else frame.INIT_WINDOW_SIZE_VER)
        else:
            frame.SetSize(frame.FULL_WINDOW_SIZE_HOR if get_config("is_advanced_mode") else frame.INIT_WINDOW_SIZE_HOR)
        frame.Show()
        return True

    def OnExit(self):
        return 0


if __name__ == '__main__':
    print("\n\nyou can't run this file directly, run boot.pyw instead.")
    print("Now the help utility will be opened in a second. You can search the document of the APIs")
    print()
    help()
