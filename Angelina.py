"""
this is the main GUI interface of the program.

author: Weizheng Wang
build time: 11/9/2019 19:45

Copyright (C) 2020  Weizheng Wang

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

import os, sys
import wx
import time
import cross
import settings
# noinspection PyUnresolvedReferences
from math import *  # DO NOT DELETE THIS
from config.config_library import get_config, set_config, save_config, clear_vars, set_config_pool, debug_log, printf

HELP_WEBSITE = 'https://github.com/EPIC-WANG/Datanalyze'  # the website if user tapped HELP


# noinspection PyUnusedLocal,DuplicatedCode,PyAttributeOutsideInit
# the GUI contains too many duplicated codes, and you know why.
class Tempest(wx.Frame):
    dpi = get_config("dpi_scale", 1.0)
    INIT_WINDOW_SIZE_HOR: tuple  = (420 * dpi, 320 * dpi)
    INIT_WINDOW_SIZE_VER: tuple  = (420 * dpi, 320 * dpi)
    FULL_WINDOW_SIZE_HOR: tuple  = (750 * dpi, 372 * dpi)
    FULL_WINDOW_SIZE_VER: tuple  = (460 * dpi, 830 * dpi)
    MIN_WINDOW_SIZE_HOR: tuple   = (400 * dpi, 170 * dpi)
    MIN_WINDOW_SIZE_VER: tuple   = (400 * dpi, 170 * dpi)
    MAX_CHOICE_SIZE: tuple       = (-1       , 36  * dpi)
    
    @debug_log
    def __init__(self) -> None:
        """
        The
        """
        self.frame = wx.Frame.__init__(self, parent=None, title="Main Frame")
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Center()
        self.set_font()
        self.set_menu_bar()
        self.set_panel()

    def set_font(self):
        self.font_tc_equ = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Consolas")
        self.winfont = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Segoe UI")
        # , font=self.winfont

    @debug_log
    def set_menu_bar(self):
        menu_bar = wx.MenuBar()
        """"""
        appmenu = wx.Menu()
        menu_bar.Append(appmenu, "&Program")
        menu_close = appmenu.Append(wx.ID_ANY, "Exit")
        menu_restart = appmenu.Append(wx.ID_ANY, "Restart")
        menu_restart_and_reset = appmenu.Append(wx.ID_ANY, "Reset and restart")
        menu_settings = appmenu.Append(wx.ID_ANY, "Settings")
        self.Bind(wx.EVT_MENU, self.on_close, menu_close)
        self.Bind(wx.EVT_MENU, self.on_restart, menu_restart)
        self.Bind(wx.EVT_MENU, self.on_restart_and_reset, menu_restart_and_reset)
        self.Bind(wx.EVT_MENU, self.on_settings, menu_settings)

        """"""
        plotfilemenu = wx.Menu()
        menu_bar.Append(plotfilemenu, "&File")
        menu_save_figure = plotfilemenu.Append(wx.ID_ANY, "Quick save last figure")
        menu_save_config = plotfilemenu.Append(wx.ID_ANY, "Save config")
        menu_display_config = plotfilemenu.Append(wx.ID_ANY, "Display config")
        menu_clear_config = plotfilemenu.Append(wx.ID_ANY, "Clear config")
        self.Bind(wx.EVT_MENU, self.on_save_figure, menu_save_figure)
        self.Bind(wx.EVT_MENU, self.on_save_config, menu_save_config)
        self.Bind(wx.EVT_MENU, self.on_display_config, menu_display_config)
        self.Bind(wx.EVT_MENU, self.on_clear_config, menu_clear_config)
        """"""
        advancedmenu = wx.Menu()
        menu_bar.Append(advancedmenu, "&Advanced")
        menu_open_config_commandline = advancedmenu.Append(wx.ID_ANY, "Open config commandline")
        menu_reset_config = advancedmenu.Append(wx.ID_ANY, "Reset config")
        menu_abort = advancedmenu.Append(wx.ID_ANY, "Abort the program")
        self.Bind(wx.EVT_MENU, self.on_open_config_commandline, menu_open_config_commandline)
        self.Bind(wx.EVT_MENU, self.on_reset_config, menu_reset_config)
        self.Bind(wx.EVT_MENU, self.on_abort, menu_abort)
        """"""
        helpmenu = wx.Menu()
        menu_bar.Append(helpmenu, "&Help")
        menu_tutorial = helpmenu.Append(wx.ID_ANY, "Tutorial")
        menu_about = helpmenu.Append(wx.ID_ANY, "About")
        self.Bind(wx.EVT_MENU, self.on_tutorial, menu_tutorial)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        """"""

        self.SetMenuBar(menu_bar)

    # noinspection PyAttributeOutsideInit
    @debug_log
    def set_panel(self):
        self.panel = wx.Panel(parent=self)
        dpi = self.dpi
        self.__panel_hbox_1_l1()
        self.__panel_hbox_1_l2()
        self.hbox_1_l3()
        self.box_comp_main()
        self.trig_show_basic_opt()

    # noinspection PyAttributeOutsideInit
    def __panel_hbox_1_l1(self):
        panel, dpi = self.panel, self.dpi
        self.create_new_fig = wx.Button(panel, label='start new', size=(-1, 60 * dpi))
        self.create_new_fig.Bind(wx.EVT_BUTTON, self.on_create_new_fig)
        self.start_plot_btn = wx.Button(panel, label='continue', size=(-1, 60 * dpi))
        self.start_plot_btn.Bind(wx.EVT_BUTTON, self.start_plot_button)
        self.settings_btn = wx.Button(panel, label='settings', size=(-1, 22 * dpi))
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

    # noinspection PyAttributeOutsideInit,SpellCheckingInspection
    def __panel_hbox_1_l2(self):
        me = self
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
                'statictext3_1', 'statictext3_2', 'statictext3_3', 'statictext3_4', 'statictext3_5', 'statictext3_6',
                'statictext3_8', 'statictext3_9', 'self.input9_xllim', 'self.input10_xrlim',
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
    def hbox_1_l3(self):
        me = self
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

    def box_comp_main(self):
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

    @staticmethod
    @debug_log
    def on_restart(event=None):
        python: str = sys.executable
        os.execl(python, python, *sys.argv)

    @debug_log
    def on_clear_config(self, event=None):
        dlg = wx.MessageDialog(self.panel, "Do You Want to clear the user variables?", "reset",
                               style=wx.YES_NO | wx.NO_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            clear_vars(save = True)
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
    def on_open_config_commandline(event=None):
        try:
            os.startfile(r"config\new_config_library.py")
        except IOError or WindowsError:
            os.startfile(r"config\new_config_library.pyc")

    @debug_log
    def on_restart_and_reset(self, event=None):
        self.on_clear_config()
        self.on_restart()

    @staticmethod
    @debug_log
    def on_about(event=None):
        wx.MessageBox("""Datanalyze  Copyright (C) 2020  Weizheng Wang
This program comes with ABSOLUTELY NO WARRANTY; for details, please read LICENSE.txt.
The copyright of this software is limited by the GNU GENERAL PUBLIC LICENSE.

This is a mathematical plotting software developed by using python. 
""")

    @staticmethod
    @debug_log
    def on_abort(event=None):
        os.abort()

    @staticmethod
    def on_settings(event=None):
        settings_frame = settings.Storm()
        settings_frame.Show()

    @debug_log
    def trig_set_basic_opt(self):
        """
        set the value of the
        """
        colour_list = [self.colour_opt[selected_colour] for selected_colour in self.colourbox.GetSelections()]
        set_config_pool(colour=colour_list if colour_list else ['black'])
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
        return bool(self.tc_equ.GetValue().replace('please input your math equation or commands in here.', '') \
                    .replace('\n', '').lstrip())

    @debug_log
    def start_plot_button(self, event=None):
        self.trig_set_basic_opt()
        inputed_function: str = self.tc_equ.GetValue()
        if not self.__is_runable():
            wx.MessageBox("please input your math equation or commands in the box!")
            return None
        
        printf(f"python_mode = {(python_mode := self.input_syntax.GetValue())}", self_=self.start_plot_button)
        
        if inputed_function != '':
            current_line = 'unknown'
            function = 'unknown'
            try:
                if python_mode is False: # it is none python mode
                    current_line = 1
                    function: str  # the input equation in each line
                    for function in inputed_function.split('\n'):
                        if not function.isspace() and function != '':
                            
                            printf(f"{function=}", self_=self.start_plot_button)
                            cross.interpret_to_falcon(function, False)
                        current_line += 1
                    cross.show()
                
                else:
                    printf(f"{inputed_function=}", self_=self.start_plot_button)
                    cross.interpret_to_falcon(inputed_function, True)
                    wx.MessageBox("Done!")
                
            except KeyboardInterrupt:
                printf(f"User had canceled the operation in line {current_line}", self_ = self.start_plot_button)
                wx.MessageBox(f"User had canceled the operation in line {current_line}")
            except Exception as _:
                printf(f"A error occurs during the executing progress in line {current_line}: '{function}': {str(_)}", self_=self.start_plot_button)
                wx.MessageBox(f"A error occurs during the executing progress in line {current_line}: '{function}' \n {str(_)}")
            cross.show()
        return None

    def on_tc_equ_left_down(self, event=None):
        if self.tc_equ.GetValue() == 'please input your math equation or commands in here.':
            self.tc_equ.Clear()

    def on_create_new_fig(self, event=None):
        if self.input_syntax.GetValue() is False:
            cross.new_fig()
        self.start_plot_button()

    @debug_log
    def __toggle_advanced_config(self, is_advanced_mode: bool):
        if not is_advanced_mode:
            # set the value to the default
            self.calc_count.SetValue(str(get_config("$default_calc_count")))
            self.figspine.SetValue(get_config("$default_figspine"))
            self.cho5_linestyle.SetValue(get_config("$default_linestyle"))

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
                               "Do You Want to reset and restart the program? this will fix the issue of the program.",
                               "reset",
                               style=wx.YES_NO | wx.NO_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            os.remove(r"config\bootconfig.cfg")
            python = sys.executable
            os.execl(python, python, *sys.argv)

    @staticmethod
    @debug_log
    def on_save_figure(event=None):
        try:
            wx.MessageBox(f"saved figure '{cross.save()}' successful.")
        except Exception as _:
            wx.MessageBox(f"saved figure failed, {_}")

    @staticmethod
    @debug_log
    def on_tutorial(event=None):
        import webbrowser
        webbrowser.open(HELP_WEBSITE)
        wx.MessageBox("tutorial has opened in your web browser.")


class App(wx.App):

    @debug_log
    def OnInit(self):
        frame = Tempest()
        if get_config("is_vertical_screen"):
            frame.SetSize(frame.FULL_WINDOW_SIZE_VER if get_config("is_advanced_mode") else frame.INIT_WINDOW_SIZE_VER)
        else:
            frame.SetSize(frame.FULL_WINDOW_SIZE_HOR if get_config("is_advanced_mode") else frame.INIT_WINDOW_SIZE_HOR)
        frame.Show()
        return True

    def OnExit(self):
        return 0
