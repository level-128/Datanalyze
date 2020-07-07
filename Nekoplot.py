"""
this is a matplotlib-based fast plotting lib.
THIS LIBRARY MUST RUN IN THE DATANALYZE ENVIRONMENT!

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

from typing import Union, List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import wx
from numpy import *

from config.config_library import get_config, debug_log, fprintf, config, poolobject

if float(matplotlib.__version__[:3]) < 3.1:
    raise ImportError("matplotlib version MUST above 3.1.0. Please install the correct version of matplotlib.")

_ = matplotlib.collections.LineCollection
matplotlib.use("WXAgg")

DPI_SCALE: float = config["dpi_scale"]

TRANS_TO_2D_MESSAGE: str = "Your next function is two-dimensional and needs to be drawn on a two-dimensional " \
                           "coordinate axis. Do you want to create a new coordinate axis and draw it? choose CANCEL" \
                           " will abort the process."
TRANS_TO_3D_MESSAGE: str = "Your next function is three-dimensional and needs to be drawn on a three-dimensional " \
                           "coordinate axis. Do you want to create a new coordinate axis and draw it? choose CANCEL" \
                           " will abort the process."
TRANS_TO_POLAR_MESSAGE: str = "Your next function is polar and needs to be drawn on a polar " \
                           "coordinate axis. Do you want to create a new coordinate axis and draw it? choose CANCEL" \
                           " will abort the process."

# init functions

I = complex(0, 1)
ln = np.log
log = np.log10


class falcon:
    """create a new fig"""
    def __init__(self):
        self.colour = poolobject(config['colour'])

    @staticmethod
    def __show_message_window(content: str, select_id, /, title: str = 'warning'):
        """
        display the message and return the selected wx.ID
        :return wx.ID
        """
        __frame = wx.Frame()
        dlg = wx.MessageDialog(__frame, content, title, style=select_id)
        option = dlg.ShowModal()
        __frame.Destroy()
        return option

    @staticmethod
    def __get_meshgrid() -> Tuple[ndarray, ndarray]:
        x = linspace(get_config("xllim"), get_config("xrlim"), get_config("calc_count"))
        y = linspace(get_config("yllim"), get_config("yrlim"), get_config("calc_count"))
        # noinspection PyTypeChecker
        return meshgrid(x, y)  # this type is correct.

    @staticmethod
    @debug_log
    def __get_index(element: list, index: int, default: any = None):
        try:
            return element[index]
        except:
            return default

    @staticmethod
    @debug_log
    def show():
        plt.show()

    @staticmethod
    def process_2d_equ(equation: str) -> str:
        equal_list = equation.split('=')
        if len(equal_list) == 1:
            return equal_list[0]
        elif len(equal_list) == 2:
            return f"-({equal_list[0]})+{equal_list[1]}"
        else:
            raise SyntaxError("the equation has more than one equal sign.")

    @staticmethod
    def process_3d_equ(equation: str) -> str:
        return equation[4:]  # eliminate ' z ='

    @staticmethod
    def process_2d_polar_equ(equation: str) -> str:
        equation = equation.replace(' theta ', ' x ').replace(' r ', ' y ')
        return falcon.process_2d_equ(equation)

    @debug_log
    def __new_fig3d(self):

        self.fig_type = "3d"  # the last plotted figure
        # if i do nothing, the fig will show at this point.
        self.fig = plt.figure(figsize=(8, 8), dpi=get_config("dpi", 80) * DPI_SCALE)
        self.ax = self.fig.gca(projection='3d')
        self.ax.set_xlim3d(get_config("xllim", -5), get_config("xrlim", 5))
        self.ax.set_ylim3d(get_config("yllim", -5), get_config("yrlim", 5))
        self.ax.set_zlim3d(get_config("zllim", -5), get_config("zrlim", 5))
        self.fig.tight_layout()

        if get_config("show_org_point", True):
            self.ax.scatter(0, 0, 0, color="black")

    @debug_log
    def __new_fig2d(self) -> None:
        """
        create a new 2d fig
        """
        # if i do nothing, the fig will show at this point.
        self.fig = plt.figure(figsize=(8, 8), dpi=get_config("dpi", 80) * DPI_SCALE)
        self.ax = self.fig.gca()
        self.fig_type = "2d"
        self.ax.set_xlim(get_config("xllim", -5), get_config("xrlim", 5))
        self.ax.set_ylim(get_config("yllim", -5), get_config("yrlim", 5))

        if get_config("aspect_equal", False):
            self.ax.set_aspect('equal')
        if get_config("is_grid", True):
            self.ax.grid()
        if get_config("figspine", "normal") != "normal":
            self.ax.spines['top'].set_color('none')
            self.ax.spines['right'].set_color('none')
            if get_config("figspine", "normal") == "coord":
                self.ax.spines['bottom'].set_position(('data', 0))
                self.ax.spines['left'].set_position(('data', 0))
            elif get_config("figspine", "normal") == "sign":
                self.ax.spines['bottom'].set_color('none')
                self.ax.spines['left'].set_color('none')

        self.ax.set_title(get_config("title", ''))
        self.ax.set_xlabel(get_config('xlabel', 'X'))
        self.ax.set_ylabel(get_config('ylabel', 'Y'))
        self.fig.tight_layout()

        # range

    @debug_log
    def __new_fig2d_polar(self) -> None:
        self.fig = plt.figure(figsize=(8, 8), dpi=get_config("dpi", 80) * DPI_SCALE)
        self.ax = self.fig.gca(projection="polar")
        self.fig_type = '2d_polar'

        self.ax.set_title(get_config("title", ''))
        self.ax.set_xlabel(get_config('xlabel', 'X'))
        self.ax.set_ylabel(get_config('ylabel', 'Y'))
        self.fig.tight_layout()

    @debug_log
    def __is_new_fig(self, new_fig_type: str, force_new_fig: bool=False):
        try:
            assert self.fig  # look the figure is created or not
            if get_config("new_fig", False) or force_new_fig:
                raise AttributeError("a fig was created because of force config set by policy.")

            elif self.fig_type != new_fig_type:
                option = self.__show_message_window(TRANS_TO_POLAR_MESSAGE, wx.OK | wx.CANCEL | wx.OK_DEFAULT)

                fprintf(f"{new_fig_type} change fig event raised. {option=}", self_=self.__is_new_fig)
                if option == wx.ID_OK:
                    if new_fig_type == '2d':
                        self.__new_fig2d()
                    elif new_fig_type == '3d':
                        self.__new_fig3d()
                    else:
                        self.__new_fig2d_polar()
                elif option == wx.ID_CANCEL:
                    raise KeyboardInterrupt("User has canceled this operation.")

        except AttributeError as _:
            fprintf(f"No {new_fig_type} figure left, creating fig. {_})", self_=self.__is_new_fig)
            if new_fig_type == '2d':
                self.__new_fig2d()
            elif new_fig_type == '3d':
                self.__new_fig3d()
            else:
                self.__new_fig2d_polar()

    @debug_log
    def plot_3d(self, raw_equation, force_new_fig=False):
        self.__is_new_fig('3d', force_new_fig)
        equation = self.process_3d_equ(raw_equation)
        x, y = self.__get_meshgrid()

        try:
            self.ax.plot_wireframe(x, y, eval(equation), antialiased=get_config("is_antialiased"),
                                   color=self.colour.get_poolobj_value(), rcount=30, ccount=30,
                                   alpha=get_config("alpha") * 0.38)
        except Exception as error:
            raise UserWarning(f"function '{equation}' syntax illegal. {error}")
        finally:
            del x, y

    def __plot_2d_base(self, x, y, equation: str) -> None:
        plt.contour(x, y, eval(equation), 0, linewidths=get_config("linewidth"),
                    colors=self.colour.get_poolobj_value(),
                    linestyles=get_config("linestyle", ),  # ['-','--','-.',':']
                    antialiased=get_config("is_antialiased"),
                    alpha=get_config("alpha"),
                    )
        del x
        del y

    @debug_log
    def __plot_2d(self, raw_equation: str, force_new_fig=False):
        self.__is_new_fig('2d', force_new_fig)
        equation = self.process_2d_equ(raw_equation)
        x, y = self.__get_meshgrid()
        try:
            self.__plot_2d_base(x, y, equation)
        except Exception as error:
            raise UserWarning(f"function '{raw_equation}' syntax illegal. {error}")

    @debug_log
    def __plot_2d_polar(self, raw_equation: str, force_new_fig=False) -> None:
        self.__is_new_fig('2d_polar', force_new_fig)
        equation = self.process_2d_polar_equ(raw_equation)
        x = linspace(get_config("xllim"), get_config("xrlim"), _ := get_config("calc_count"))
        y = linspace(0, get_config("yrlim"), _)  # in the polar equation, the yllim MUST be 0!
        x, y = meshgrid(x, y)  # this type is correct.
        try:
            self.__plot_2d_base(x, y, equation)
        except Exception as error:
            raise UserWarning(f"function '{raw_equation}' syntax illegal. {error}")

    def plot_2d(self, raw_equation: str, force_new_fig=False):
        if (_ := (raw_equation.find(' r ') == -1)) and raw_equation.find(' theta ') == -1:
            # the fig is 2D
            self.__plot_2d(raw_equation, force_new_fig=force_new_fig)
        elif not _ and raw_equation.find(' theta ') != -1:
            self.__plot_2d_polar(raw_equation, force_new_fig=force_new_fig)
        else:
            print(raw_equation)
            raise SyntaxError(
                "vague variables occurs in equation. Check variable usage (for example, mixed 'theta' / 'x' and 'r' / "
                "'y' in a equation)")

    @debug_log
    def __plot_vectors_2d(self,
                          vector: List[List[Union[int, float]]],
                          start_at: List[List[Union[int, float]]],
                          force_new_fig: bool = False):

        self.__is_new_fig('2d', force_new_fig)
        for plot_index in range(len(vector)):
            plot_vector, cur_start_at = vector[plot_index], start_at[plot_index]

            arrow_size = max(get_config("xrlim") - get_config("xllim"),
                             get_config("yrlim") - get_config("yllim")) * 0.02
            plt.arrow(cur_start_at[0], cur_start_at[1], plot_vector[0], plot_vector[1],
                      length_includes_head=True,
                      head_width=arrow_size, head_length=arrow_size * 2, ec=self.colour.get_poolobj_value(),
                      alpha=get_config("alpha"), width=get_config("linewidth") * 0.05,
                      fc=self.colour.get_poolobj_value())

    @debug_log
    def __plot_vectors_3d(self,
                          vector: List[List[Union[int, float]]],
                          start_at: List[List[Union[int, float]]], /,
                          force_new_fig: bool = False):

        self.__is_new_fig('3d', force_new_fig)
        for plot_index in range(len(vector)):
            plot_vector, cur_start_at = vector[plot_index], start_at[plot_index]

            X, Y, Z = np.meshgrid(self.__get_index(cur_start_at, 0, 0)
                                  , self.__get_index(cur_start_at, 1, 0)
                                  , self.__get_index(cur_start_at, 2, 0))
            x = self.__get_index(plot_vector, 0, 0)
            y = self.__get_index(plot_vector, 1, 0)
            z = self.__get_index(plot_vector, 2, 0)
            self.ax.quiver(X, Y, Z, x, y, z, color=self.colour.get_poolobj_value(), arrow_length_ratio=0.2,
                           alpha=get_config("alpha"))

    @debug_log
    def plot_vectors(self, input_str: str, force_new_fig=False):
        """
        Set the vectors in a acceptable and correct syntax, Then plot them according the correct dimension
        If one of the dimension count of a given vector in a nested list is larger than 2, the vector set should be plot
        in a 3D figure.
        :param force_new_fig: create a new fig and ignore the conditions
        :param input_str: The raw string, may include ";" for spiting the vectors and its starting position(s).
        :return: None
        """
        is_3d: bool
        vectors: list
        vectors_start_poz: list

        packed_vector: List[str] = input_str.split(";")  # split the vectors and the starting position.
        # if the starting position is void, [0] will be placed and the plotting lib will auto fill other 0s to match the
        # dimension of the vector(s).
        vectors_start_poz = [0, 0, 0] if len(packed_vector) == 1 else eval(packed_vector[1])

        vectors = eval(packed_vector[0])  # using eval to execute all the numpy variables and functions in the vectors.
        # get the max dimension f the given vector(s). the max dimension shouldn't exceed 3
        assert (max_dim := max(len(_) for _ in (vectors if type(vectors[0]) == list else [vectors]))) in (2, 3)
        # packing all the vectors into nested lists.
        if type(vectors[0]) in (int, float):
            vectors = [vectors]
        if type(vectors_start_poz[0]) is not list:
            vectors_start_poz = [vectors_start_poz]
        # expand the vectors_start_poz and
        assert (is_same_start := ((_ := len(vectors_start_poz)) == 1)) or _ == len(vectors)
        if is_same_start:
            vectors_start_poz *= len(vectors)

        self.__plot_vectors_3d(vectors, vectors_start_poz,force_new_fig=force_new_fig) \
            if max_dim == 3 else \
            self.__plot_vectors_2d(vectors, vectors_start_poz, force_new_fig=force_new_fig)

    @debug_log
    def export_fig(self, filetype=get_config("save_format", "svg"), filedir='figure'):
        assert filetype in ['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif',
                            'tiff']
        plt.savefig(f"{filedir}.{filetype}", format=filetype)
