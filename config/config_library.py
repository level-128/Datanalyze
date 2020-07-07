"""
this is a modifiable layer, providing functions such as:

1. load and store user variables during the application pre boot session and the period when handling SystemExit
exception.

2. modify variables and passing them between functions and methods. when the application suddenly crashed, the variables
could be stored, providing possible recovery solutions.

3. provides easy logging by adding decorator '@debug_log'. the log will record the time(start and end) and the sequence
that triggered by function/method(s).

4. providing 'fprintf' to print the custom logging message to the console and log file.

5. providing custom exception, allows values to pass through when raised.

6. Poolobject is a iterable object, provided in here, representing a infinite sequence. it could be used as if it is a
generator. giving a iterable object, the Poolobject will loop the object endlessly.


This file was created when i was developing Datanalyze, PythonLinearAlgebra and my experiment of Independent Research
Project. these projects are used for my school project and my own interest. Special thanks to Xu Xiang, Wu Chuqiao for
inspiring me about the projects above.


NOTE:
DO NOT MODIFY THIS FILE UNLESS YOU ARE VERY CERTAIN ABOUT THIS AND ITS FUNCTION.
DO NOT CHANGE THE NAME OF THE APIs DUE TO THE DYNAMIC MODULE LOADING, INCLUDING 'REFACTOR' OPTION IN YOUR IDE!!!!
    if you do so, the dynamic module, which originally does NOT belong to this project, under folder 'Lib' may
    malfunction when the script tries to call the APIs.


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

import copy
import os
import platform
import sys
import time
import json
from abc import abstractmethod
from collections.abc import Iterable, Callable, Container
from json import JSONDecodeError
from typing import TextIO, Union, Any

__version__ = '20.06.28'  # the last modify date

FILE_DIR: str = r"config\bootconfig.cfg"
LOG_DIR: str = r"config\cfg_log.log"

log_file: Union[None, TextIO] = None
start_time: Union[float, None] = None

DEFAULT_VARS: dict = {

    # the GUI settings
    "$GUI_force_set_zoom_ratio": None,  # manually set self.gui value, none or float
    "$GUI_force_set_zoom_bias_add": 0,  # self.gui + constant
    "$GUI_force_set_zoom_bias_multiply": 1,  # self.gui * constant
    "$GUI_os_process_dpi_awareness": 1,  # os GUI zoom behaviour, int or False
    "$GUI_is_vertical_screen": False,

    # the fig settings
    "$xllim": '-5',
    "$xrlim": '5',
    "$yllim": '-5',
    "$yrlim": '5',
    "$zllim": '-5',
    "$zrlim": '5',

    "$title": '',
    "$xlabel": 'X',
    "$ylabel": 'Y',

    "$linewidth": 1,
    "$linestyle": 'solid',
    "$alpha": 1,
    "$figspine": "coord",  # coord, sign, normal, L
    "$calc_count": 500,

    "$is_antialiased": True,
    "$is_grid": True,
    "$is_aspect_equal": False,

    # policy settings
    "$save_format": "svg",
    "$is_advanced_mode": False,
    "$is_python_input": False,
    "$is_print_log": True,
    "$is_save_log": True,

    # fast compute settings
    "$is_AOT": False,
    "$is_parallel": False,
    "$is_float32": False,
    "$is_fast_math": False
}

"""custom exceptions are generated below"""


class RaisedExit(Exception):
    """
    when using this exception, make sure that this exception will be catch in somewhere.
    """

    def __init__(self, *args):
        self.args = args


class EnvInitFail(Exception):
    """
    use when there is an failure which prevent the software to boot normally.
    """

    def __init__(self, /, module_name=__name__, ignore_behaviour=False, message=None):
        self.module_name = module_name
        self.ignore_behaviour = ignore_behaviour
        self.message = message


class RaisedCritical(Exception):
    """
    raised when the software enters a critical state and requires sudden abort
    """

    def __init__(self, /, message: str = 'unrecorded', module_name: str = 'unknown'):
        global log_file
        fprintf(f"the RaisedCritical exception has raised due to {message} in {module_name}")
        if log_file is not None:
            log_file.close()
        exit(1)


"""debug and logging functions below"""


def __new_log() -> None:
    """
    create a log file if the log policy is enabled
    :return: None
    """
    global log_file, start_time
    log_file = open(LOG_DIR, 'w', buffering=2, encoding='utf-8')
    log_file.write(f"This is the log file of the Datanalyze, version: {__version__}, ")
    log_file.write(f'platform = {platform.platform()}, version = {platform.version()}\n------------\n')
    log_file.write("The log file is created due to the global settings_frame of the software. To close it, \nplease mod"
                   "ify the bootconfig.cfg by hand or use 'config['is_save_log'] = False' in the command line.\n-------"
                   "-----\n")
    start_time = time.time()
    log_file.write(f"the log record starts at {start_time}\n\n")
    return None


def fprintf(content, /, flush: bool = False, end: str = '\n', self_: Union[str, Any] = "NotIndicated") -> None:
    """
    print the content into the console and write it into the log file.
    :param content: The massage for output
    :param flush: flush the output
    :param end: same as print
    :param self_: the function/method which need to be logged.
    :return: None
    """
    if IS_PRINT_LOG:
        print(content, flush=flush, end=end)
    if IS_SAVE_LOG:
        log_file.write(f'{time.time() - start_time} in {self_} --> {content}\n')


def debug_log(input_func, message_before: str = "the event has started"):
    """
    this is used as a wrapper to record the log when calling a function automatically.
    :param input_func: the wrapper will handle this
    :param message_before: the message append before calling

    :return: a function
    """
    if IS_SAVE_LOG:
        def inner(*args, **kwargs):
            log_file.write(f'{time.time() - start_time} in {input_func} --> {message_before}\n')
            res = input_func(*args, **kwargs)
            return res

        return inner
    else:
        return input_func


"""poolobject"""


class poolobject:
    """
    this is a object which accept an iterable item and turn it into a infinite loop
    """
    __obj: list
    __calltime: int

    def __init__(self, obj: list, calltime: int = 0):
        assert isinstance(obj, Iterable)  # it must be iterable
        assert len(obj)  # it must not be empty
        self.__obj = obj
        self.__calltime = calltime

    def __repr__(self):
        return f"poolobject({self.__obj})"

    def __len__(self):
        return len(self.__obj)

    def __iter__(self):
        """
        returns a iterator which will never stop, which means StopIteration will never be raised.
        :return: None
        """
        while True:
            yield from self.__obj

    def __next__(self):
        raise Exception("it is not recommended to use next(), use get_poolobj_value() instead")

    @abstractmethod
    def is_poolobject(self):
        """
        THIS METHOD ONLY USED FOR DETECTING THE EXISTENCE OF THE POOLOBJECT AND USED IN THE DUCK TYPE.
        """
        return True

    def get_poolobj_value(self, /, increase_calltime: bool = True) -> any:
        """
        this is used to replace next(), which provides choices of
        :param increase_calltime:
        :return:
        """
        temp = self.__obj[self.__calltime]
        if increase_calltime and self.__calltime < len(self.__obj) - 1:
            self.__calltime += 1
        else:
            self.__calltime = 0
        return temp

    def get_poolobj(self):
        return copy.deepcopy(self.__obj)

    def get_poolobj_raw(self):
        return self.__obj

    @classmethod
    def set_poolobj(cls, obj: list, calltime: int = 0):
        return cls(obj, calltime)

    def get_call_time(self) -> int:
        return self.__calltime

    def set_call_time(self, calltime: int):
        if calltime < 0:
            raise ValueError("calltime must >= 0.")
        if calltime >= (_ := len(self.__obj)):
            raise ValueError(f"call time must smaller than {_}")
        self.__calltime = calltime

    def append(self, item: any):
        self.__obj.append(item)

    def remove(self, content):
        self.__obj.remove(content)

    def pop(self, index: int):
        self.__obj.pop(index)


class config:
    """
    # This class is designed for passing parameters between methods
    # Demo:

    from config.config_library import config, get_config, set_config
    """

    __config_dict: Union[dict, None] = None

    def __init__(self):
        if not os.path.exists(FILE_DIR):
            self.__build_config_file()
        self.refresh_file()

    def __setitem__(self, key: str, value: Union[int, float, str, list, tuple, dict, None, bool]) -> None:
        """
        set the value 'config["config_name"] = config_value'
        the value type, for converting to the JSON object, must be one of them in
        (int, float, str, list, tuple, dict, None, bool)
        the __setitem__ will create a new value or change the existing value.
        a key starts with '$' is constant value. You can't create a new value by this key pattern.

        :param key : the key of the parameter
        :param value: the value which you decided to set

        :return : None

        :raises : ValueError if the type of 'key' and 'value' are invalid.
                  KeyError if the you tried to create a default value (start with '$')
        """
        if type(key) is not str:
            raise ValueError("the type of the key must be string.")
        # make sure that the value could be transfer to JSON format
        if type(value) not in (_ := (int, float, str, list, tuple, dict, bool)) and value is not None:
            raise ValueError(f"the type of the value must be {_} or None, get {type(value)} instead.")

        if key[0] == '$' and key not in self.__config_dict:
            fprintf(_ := "could not add default or pool variable, or using database preserve letters.",
                    self_=self.__setitem__)
            raise KeyError(_)
        self.__config_dict[key] = value

    def __getitem__(self, key: str) -> None:
        """
        get value by 'config["config_name"]'.
        if the key, which initially does not start with $, does not exist, return config['$' + key] instead.

        :param key: the key of the value

        :return : None

        :raises : KeyError for invalid key
                  ValueError for type(key) is not str
        """
        if type(key) is not str:
            raise ValueError("the type of the key must be string.")

        try:
            return self.__config_dict[key]
        except KeyError:
            if key[0] == '$':
                raise KeyError("the default variable does not exist")
            return self.__config_dict['$' + key]  # let the KeyError go

    @staticmethod
    def reset_config():
        """
        reset all the value into default value by removing config\bootconfig.cfg
        requires restart. During restart, the config\bootconfig.cfg will be recreated.

        :return : None

        :raise : SystemExit
        """
        try:
            __import__("os").remove(FILE_DIR)
        except IOError or SystemError or WindowsError:
            fprintf(_ := f'Failed to remove {FILE_DIR}, please remove the file manually. ', self_=config.reset_config)
            raise EnvInitFail(message=_)
        fprintf(_ := f"core lib requires to exit the program for resetting the config file.", self_=config.reset_config)
        raise SystemExit(_)

    def get_config(self, cfg_name: str, default: any = None) -> any:
        """
        similar with config.__getitem__, but provides a default value
        No exceptions will be raised. If the key does not exist and param 'default' is empty, return None.

        :param cfg_name: key
        :param default: the return value if the key does not exist.

        :return: Any

        :raise: ValueError if cfg_name is not str
        """
        try:
            return self.__getitem__(cfg_name)
        except KeyError:
            fprintf(f"error key {cfg_name} when calling {self.get_config}, the key does not exist, return default.",
                    self_=self.get_config)
            return default

    def set_config(self, name: str = None, value=None, **kwargs) -> None:
        """
        similar with config.__setitem__, but provides faster operation when deal with a large amount of data.
        :param name: key
        :param value: value
        :param kwargs: providing faster operation for multiple keys, such as 'set_config(my_var='green', var2=10)'

        :return: None

        :raises: ValueError if the type of 'key' and 'value' are invalid.
                 KeyError if the you tried to create a default value (start with '$')
        """
        if name is not None and value is not None:
            self.__setitem__(name, value)
            return
        for key in kwargs:
            self.__setitem__(key, kwargs[key])

    def save_config(self):
        """
        save the config into the config file
        :return: None
        """
        __config_raw_file = open(FILE_DIR, 'w', encoding='utf-8')
        __config_raw_file.write(json.dumps(self.__config_dict, indent=0))
        __config_raw_file.close()

    @staticmethod
    def __build_config_file():
        """
        rebuild the config file when the file is deleted.
        :return: None
        """
        _ = open(FILE_DIR, 'w')
        _.write(json.dumps(DEFAULT_VARS, indent=0))
        _.close()

    def clear_vars(self, save: bool = True) -> None:
        """
        rebuild the config file when the file is deleted.
        :return: None
        """
        for x in self.__config_dict.keys():
            if x[0] != "$":
                self.__config_dict.pop(x)
        if save:
            self.save_config()

    def refresh_file(self):
        """
        read the file and refresh the config
        if failed to read, the config file will be deleted and the program will exit.
        :return:
        """
        __config_raw_file = open(FILE_DIR, 'r', encoding='utf-8')
        try:
            self.__config_dict = dict(json.loads(__config_raw_file.read()))
        except JSONDecodeError as e:
            print("error load JSON config file. This may due to software bug or unexpected exit. Do not abort the "
                  "program unless needed.")
            print(e)
            __config_raw_file.close()
            os.remove(FILE_DIR)
            os.abort()
        else:
            __config_raw_file.close()


"""
running process below
"""
if __name__ == '__main__':
    raise EnvInitFail("this lib isn't used for run directly. If you want to perform a unit test, use another file and "
                      "import this instead.")

config = config()  # you can't define a new instance from now.

# optimize for imports.
clear_vars = config.clear_vars
get_config = config.get_config
reset_config = config.reset_config
save_config = config.save_config
set_config = config.set_config

IS_SAVE_LOG = config["is_save_log"]
IS_PRINT_LOG = config['is_print_log']

if IS_SAVE_LOG:
    __new_log()
