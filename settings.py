"""
Created on Sat Aug 10 22:26:12 2019

@author: Wang7

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
import os
import sys
from typing import overload, Union, List, Tuple
import wx
from config.config_library import save_config, fprintf, debug_log, config, reset_config

STATIC_WINDOW_SIZE: tuple = 350, 620
STATIC_SMALL_GAP: float = 40.0
STATIC_MID_GAP: float = 50.0
STATIC_LARGE_GAP: float = 70.0

CONST_SMALL_GAP: int = 1
CONST_MID_GAP: int = 2
CONST_LARGE_GAP: int = 3


class Storm(wx.Frame):
    dpi_scale: float = config["dpi_scale"]
    fprintf(f"the settings opened with {dpi_scale=} on {__name__}")

    x = lambda me, _, __: (int(_ * me.dpi_scale), int(__ * me.dpi_scale))

    ui_xpoz_plus: int = 0  # used to set the start xpoz for the elements.

    current_poz_ = 2  # used to set the start ypoz for the elements

    @debug_log
    def __init__(self):
        wx.Frame.__init__(self, None, title='Settings Frame')
        wx.Frame.SetBackgroundColour(self, 'white')
        self.panel = wx.ScrolledWindow(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSize(_ := (STATIC_WINDOW_SIZE[0] * self.dpi_scale, STATIC_WINDOW_SIZE[1] * self.dpi_scale))
        self.SetMaxSize(_)
        self.SetMinSize(_)
        self.Center()

        self.set_font()
        self.set_panel()
        self.panel.SetScrollbars(-1, 12 * self.dpi_scale, -1, (self.current_poz_ + 50) / 12)

        self.panel_elements = []
        for keys in self.__dict__:
            if keys.startswith('input'):
                self.panel_elements.append(keys)

        self.display_value_to_frame()

    def get_next_poz(self, const: int) -> int:
        """
		this is the recommended method for getting the position. returns the raw poz
		:param const: the constant value of the nest position
		:return: the y value of the position
		"""
        self.current_poz_ += [
            0,
            STATIC_SMALL_GAP,
            STATIC_MID_GAP,
            STATIC_LARGE_GAP] \
            [const]
        return self.current_poz_

    # noinspection PyAttributeOutsideInit
    def set_font(self):
        self.winfont = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Segoe UI")
        self.title_font = wx.Font(13, wx.MODERN, wx.ITALIC, wx.BOLD, False, "Segoe UI")
        self.large_winfont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, "Segoe UI")

    # noinspection PyAttributeOutsideInit
    def set_panel(self):

        def header():
            wx.StaticText(self.panel, pos=self.x(10, self.get_next_poz(0) + 3),
                          label="This is the setting utility of the Datanalyze. \nChange the settings are NOT "
                                "recommended, \nunless for advanced users.").SetFont(self.large_winfont)

            reset_btn = wx.Button(self.panel, pos=self.x(40, self.get_next_poz(CONST_LARGE_GAP) + 5),
                                  label="RESET ALL SETTINGS AND EXIT.", size=(300, 40))
            reset_btn.SetFont(self.winfont)
            reset_btn.Bind(wx.EVT_BUTTON, self.on_reset)

        def get_input(ypoz: Union[int, float], /, font: wx.Font = self.winfont) -> wx.TextCtrl:
            _ = wx.TextCtrl(self.panel, pos=self.x(200 + self.ui_xpoz_plus, ypoz), size=self.x(100, 22))
            _.SetFont(font)
            return _

        def get_checkbox(content: str, constant: int = CONST_SMALL_GAP, /, font: wx.Font = self.winfont):
            _ = wx.CheckBox(self.panel, pos=self.x(5 + self.ui_xpoz_plus, self.get_next_poz(constant)), label=content,
                            size=self.x(300, 35))
            _.SetFont(font)
            return _

        def get_static_text(content: str, constant: int = CONST_SMALL_GAP, /, font: wx.Font = self.winfont):
            wx.StaticText(self.panel, pos=self.x(5 + self.ui_xpoz_plus, _ := self.get_next_poz(constant)),
                          label=content).SetFont(font)
            return _

        header()

        get_static_text("figure settings: ", CONST_LARGE_GAP, font=self.title_font)

        self.input_save_format = get_input(get_static_text("default save format: "))

        self.input_linewidth = get_input(get_static_text("default linewidth: "))

        self.input_alpha = get_input(get_static_text("default alpha: "))

        self.input_is_antialiased = get_checkbox("use MSAA when rendering the figure: ", CONST_MID_GAP)

        self.input_is_grid = get_checkbox("display the grid in the figure")

        self.input_is_aspect_equal = get_checkbox("display the figure with equal aspect for all axes")

        get_static_text("display settings: ", CONST_LARGE_GAP, font=self.title_font)

        self.input_GUI_os_process_dpi_awareness = get_input(get_static_text('Set Windows DPI awareness'))

        self.input_GUI_force_set_zoom_ratio = get_input(get_static_text('zoom ratio for UI:'))

        self.input_GUI_force_set_zoom_bias_add = get_input(get_static_text('zoom added bias for UI:'))

        self.input_GUI_force_set_zoom_bias_multiply = get_input(get_static_text('zoom multiplied bias for UI:'))

        # TODO: adding this part to the settings GUI when the requirements are complete.

        """
        
        get_static_text("Compute settings", CONST_LARGE_GAP, font=self.title_font)

        get_static_text('Enable AOT for higher compute speed, but requires\n sightly longer time before compute.')

        self.input_is_AOT = get_checkbox("Enable AOT (beta)")

        get_static_text("NOTE: The options below will take effect only if \n 'Enable Auto Fast Compute' is checked.")

        get_static_text(
            'Enable Fast Math will shorten the compute cost, causing \nunreliable results. \nNOTE: THIS FEATURE'
            ' IS NOT RECOMMENDED UNLESS \nTHE RESULT ARE USED FOR REFERENCE ONLY.', CONST_LARGE_GAP)

        self.input_is_fast_math = get_checkbox("Enable Fast Math", CONST_LARGE_GAP)

        get_static_text(
            "selecting float number type. Enable float32 will decrease \nthe accuracy of the result but requires less "
            "time\n to compute.", CONST_MID_GAP)

        self.input_is_float32 = get_checkbox("Use float32", CONST_MID_GAP)

        get_static_text(
            'Perform AOT parallel in each computation. \nNOTE: THIS OPTION IS NOT RECOMMENDED, FORCE \nENABLE AOT '
            'PARALLEL WILL SPEND MORE TIME BEFORE\n'
            'THE COMPUTATION, WHICH WILL CAUSE THE TOTAL TIME \nLONGER THAN EXPECTED.', CONST_MID_GAP)

        self.current_poz_ += 45

        self.input_is_parallel = get_checkbox("Enable AOT parallel")
        
        """

        get_static_text("Other settings", CONST_LARGE_GAP, font=self.title_font)

        self.input_is_save_log = get_checkbox("record the log in the cfg_log.log file.")

        self.input_is_print_log = get_checkbox("print necessary debug content on console\n(if applicable)")

    @debug_log
    def display_value_to_frame(self):
        for element in self.panel_elements:
            eval('self.' + element).SetValue(_ if type(_ := config[element[6:]]) is bool else str(_))

    @debug_log
    def save_settings_config(self):
        for element in self.panel_elements:
            element: str
            raw_element: Union[str, bool] = eval("self." + element).GetValue()

            if type(raw_element) is bool:
                config[element[6:]] = raw_element

            elif raw_element.find('None') != -1:
                config[element[6:]] = None

            elif not (not raw_element.find('.') + 1 or not (
                    _ := raw_element.replace('.', '', 1).isdigit() or (
                    not (not (_[0] == '-') or not _[1:].isdigit())))):
                config[element[6:]] = float(raw_element)

            elif raw_element.isdigit() or (not (not (raw_element[0] == '-') or not raw_element[1:].isdigit())):
                config[element[6:]] = int(raw_element)

            else:
                config[element[6:]] = raw_element

        save_config()

    def on_reset(self, *void):
        dlg = wx.MessageDialog(self.panel, "Do You Want to reset all settings?", "Reset",
                               style=wx.YES_NO | wx.NO_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            reset_config()

    @debug_log
    def on_close(self, *void) -> None:
        dlg = wx.MessageDialog(self.panel, "Do You Want to save before exit?", "Exit",
                               style=wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT)
        option = dlg.ShowModal()
        if option == wx.ID_CANCEL:
            return None
        if option == wx.ID_YES:
            self.save_settings_config()
        self.Destroy()
