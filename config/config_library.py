"""
This file is a component of the DATANALYZE environment.
The basic API and references are provided in this file.
THE DATANALYZE ENVIRONMENT WILL NOT RUN WITHOUT THIS FILE.

DO NOT MODIFY THIS FILE UNLESS YOU ARE VERY CERTAIN ABOUT THE FUNCTIONS PROVIDED IN THIS FILE.



Copyright (C) 2018  Weizheng Wang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import sys, os
import platform
import time
from abc import abstractmethod
from typing import TextIO, Union, Any

if __name__ == '__main__':
	FILE_DIR: str = r"bootconfig.cfg"
	LOG_DIR: str = r"cfg_log.log"
else:
	FILE_DIR: str = r"config\bootconfig.cfg"
	LOG_DIR: str = r"config\cfg_log.log"

__version__ = '10.0.1.b'

global log_file
global start_time
log_file = None
start_time = 0.0

DEFAULT_VARS: dict = {
	
	# the GUI settings
	"$default_GUI_force_set_zoom_ratio"          : None,  # manually set self.gui value, none or float
	"$default_GUI_force_set_zoom_bias_add"       : 0,  # self.gui + constant
	"$default_GUI_force_set_zoom_bias_multiply"  : 1,  # self.gui * constant
	"$default_GUI_os_process_dpi_awareness"      : 1,  # os GUI zoom behaviour, int or False
	"$default_GUI_is_vertical_screen"            : False,


	# the fig settings
	"$default_xllim"                             : '-5',
	"$default_xrlim"                             : '5',
	"$default_yllim"                             : '-5',
	"$default_yrlim"                             : '5',
	"$default_zllim"                             : '-5',
	"$default_zrlim"                             : '5',

	"$default_title"                             : '',
	"$default_xlabel"                            : 'X',
	"$default_ylabel"                            : 'Y',
	
	"$default_linewidth"                         : 1,
	"$default_linestyle"                         : 'solid',
	"$default_alpha"                             : 1,
	"$default_figspine"                          : "coord",  # coord, sign, normal, L
	"$default_calc_count"                        : 500,
	
	"$default_is_antialiased"                    : True,
	"$default_is_grid"                           : True,
	"$default_is_aspect_equal"                   : False,


	# policy settings
	"$default_save_format"                       : "svg",
	"$default_is_advanced_mode"                  : False,
	"$default_is_python_input"                   : False,
	"$default_is_print_log"                      : True,
	"$default_is_save_log"                       : True,


	# fast compute settings
	"$default_is_AOT"                            : False,
	"$default_is_parallel"                       : False,
	"$default_is_float32"                        : False,
	"$default_is_fast_math"                      : False
}


class RaisedExit(Exception):
	def __init__(self, *args):
		self.args = args


class DatanalyzeBaseException(Exception):
	def __init__(self, *args):
		self.args = args


class ModelBootFail(DatanalyzeBaseException):
	def __init__(self, model=__name__, ignore_behaviour=False, message=None):
		self.model = model
		self.ignore_behaviour = ignore_behaviour
		self.message = message


class EnvInitFail(DatanalyzeBaseException):
	def __init__(self, model=__name__, ignore_behaviour=False, message=None):
		self.model = model
		self.ignore_behaviour = ignore_behaviour
		self.message = message


class DimTransHighWarning(UserWarning):
	def __init__(self, *args):
		self.args = args


class DimTransLowWarning(UserWarning):
	def __init__(self, *args):
		self.args = args


class IterationError(Exception):
	def __init__(self, *args):
		self.args = args


def printf(content, flush: bool = False, end: str = '\n', self_: Union[str, Any]="NotIndicated") -> None:
	
	if config['is_print_log']:
		print(content, flush=flush, end=end)
	if config["is_save_log"]:
		log_file.write(f'{time.time() - start_time} in {self_} --> {content}\n')


def __new_log() -> None:
	"""
	create a log file and
	:return: None
	"""
	global log_file, start_time
	log_file = open(LOG_DIR, 'w', buffering=2, encoding='utf-8')
	log_file.write(f"This is the log file of the Datanalyze, version: {__version__}, ")
	log_file.write(f'platform = {platform.platform()}, version = {platform.version()}\n------------\n')
	log_file.write("The log file is created due to the global settings_frame of the software. To close it, \nplease modify the bootconfig.cfg by hand or "
	               "use 'config['is_save_log'] = False' in the command line.\n------------\n")
	start_time = time.time()
	log_file.write(f"the log record starts at {start_time}\n\n")
	return None




def debug_log(input_func, message_before: str = "the event has started", message_after: str = "the event has ended"):
	"""
	this is used as a wrapper to record the log when calling a function automatically.
	:param input_func: the wrapper will handle this
	:param message_before: the message append before calling
	:param message_after: the message located at the end of teh calling
	:return: a function
	"""
	
	if IS_SAVE_LOG:
		def inner(*args, **kwargs):
			log_file.write(f'{time.time() - start_time} in {input_func} --> {message_before}\n')
			res = input_func(*args, **kwargs)
			log_file.write(f'{time.time() - start_time} in {input_func} --> {message_after}\n')
			return res
		return inner
	
	else:
		return input_func




class poolobject:
	__obj: list
	__calltime: int
	
	def __init__(self, obj: list, calltime: int = 0):
		assert len(obj)
		self.__obj = obj
		self.__calltime = calltime
	
	def __repr__(self):
		return f"poolobject({self.__obj})"
	
	def __len__(self):
		return len(self.__obj)
	
	def __iter__(self):
		raise IterationError('the pool object does NOT support iteration. If you want to use poolobject in a loop, '
		                     'use get_poolobj() instead.')
	
	def __next__(self):
		"""
		WARNING: it is not recommend to use next(), because poolobject will never throw StopIteration error.
		@return:the value self.__obj[self.__calltime]
		"""
		return self.get_poolobj_value()
	
	@abstractmethod
	def is_poolobject(self):
		"""
		THIS METHOD ONLY USED FOR DETECTING THE EXISTENCE OF THE POOLOBJECT AND USED IN THE DUCK TYPE.
		"""
		return True
	
	def get_poolobj_value(self, increase_calltime: bool = True) -> any:
		temp = self.__obj[self.__calltime]
		if increase_calltime and self.__calltime < len(self.__obj) - 1:
			self.__calltime += 1
		else:
			self.__calltime = 0
		return temp
	
	def get_poolobj(self):
		return self.__obj.copy()
	
	def get_poolobj_raw(self):
		return self.__obj
	
	def set_poolobj(self, obj: list, calltime: int = 0):
		self.__init__(obj, calltime)
		return self
	
	def get_call_time(self) -> int:
		return self.__calltime
	
	def set_call_time(self, calltime: int):
		if calltime < 0:
			raise ValueError("calltime must >= 0.")
		self.__calltime = calltime
	
	def add(self, item: any):
		self.__obj.append(item)
	
	def remove(self, content):
		self.__obj.remove(content)
	
	def pop(self, index: int):
		self.__obj.pop(index)


class config:
	def __init__(self):
		try:
			__config_raw_file = open(FILE_DIR, "r")
		except OSError:
			self.__build_config_file()
			__config_raw_file = open(FILE_DIR, "r")
		
		self.__config_dict: dict = self.__read_file(__config_raw_file)
		__config_raw_file.close()
		self.poolobject = poolobject
	
	def __setitem__(self, key: str, value: Any) -> None:
		"""
		set the value of the config it is same with the method set_config.
		I hope that all the new structures could use config[xxx] instead of legacy methods below, which I gonna
		abandon them in future decades.
		:param key: str ONLY!!!!!!!!!!!!!!
		:param value: Any
		:return: None
		"""
		if key[0] == '$' and key not in self.__config_dict:
			printf(_ := "could not add default or pool variable, or using database preserve letters.", self_=self.__setitem__)
			raise KeyError(_)
		self.__config_dict[key] = value
	
	def __getitem__(self, item: str):
		if item[1] == '$':
			_ = self.__config_dict[item]
		else:
			try:
				_ = self.__config_dict[item]
			except KeyError:
				_ = self.__config_dict['$default_' + item]
		try:
			assert _.is_poolobject  # an abstract method
		except AttributeError or AssertionError:
			return _
		else:
			return _.get_poolobj_value()
	
	@staticmethod
	def __build_config_file():
		_ = open(FILE_DIR, 'w+')
		_.write(str(DEFAULT_VARS) + '\n')
		_.close()
	
	# TODO: just fakin REPLACE these methods with a new one! they are NOT required anymore! I'm not gonna maintain them.
	@staticmethod
	def reset_config():
		try:
			__import__("os").remove(FILE_DIR)
		except IOError or SystemError or WindowsError:
			printf(_ := f'Failed to remove {FILE_DIR}, please remove the file manually. ', self_=config.reset_config)
			raise EnvInitFail(message=_)
		printf(_ := f"core lib requires to exit the program for resetting the config file.", self_=config.reset_config)
		raise SystemExit(_)
	
	def get_config(self, cfg_name: str, default: any = None, create_none_exist_var: bool = True):
		try:
			return self[cfg_name]
		except KeyError:
			if default is not None:
				if create_none_exist_var:
					self.__config_dict[cfg_name] = default
				return default
			else:
				printf(f"error key {cfg_name} when calling {self.get_config}, the key does not exist.", self_=self.get_config)
				raise AttributeError(f"the key: {cfg_name} does not exist.")
	
	def get_config_dict(self):
		return self.__config_dict.copy()
	
	def set_config(self, name: str = None, value=None, **kwargs) -> None:
		if name is not None and value is not None:
			self.__setitem__(name, value)
			return
		for key in kwargs.keys():
			self.__setitem__(key, kwargs[key])
	
	def set_config_pool(self, **kwargs) -> None:
		if kwargs == dict():
			return
		for key in kwargs.keys():
			if key[0] == '$' and key not in self.__config_dict:
				raise KeyError("could not add default variable or using database preserve letters.")
			self.__config_dict[key] = poolobject(kwargs[key])
	
	def save_config(self):
		_: TextIO = open(FILE_DIR, 'w+')
		_.write(
			'# DO NOT EDIT THIS BY HAND, OTHER WISE UNPREDICTABLE BEHAVIOUR MAY APPEAR!!!!!!\n# DELETE THIS FILE WILL '
			'LOST ALL THE CONFIG!!!!!!\n')
		_.write(',\n'.join(str(self.__config_dict).split(',')))
		
		_.close()
	
	def clear_vars(self, save: bool = True):
		
		for x in self.__config_dict.copy().keys():
			if x[0] != "$":
				self.__config_dict.pop(x)
		if save:
			self.save_config()
	
	@staticmethod
	def __read_file(__config_raw_file):
		return eval(__config_raw_file.read())


"""
running process below
"""

config = config()  # you can't define a new object.
clear_vars = config.clear_vars
get_config = config.get_config
get_config_dict = config.get_config_dict
reset_config = config.reset_config
save_config = config.save_config
set_config = config.set_config
set_config_pool = config.set_config_pool

build_ini_config = save_config
set_value = set_config
get_value = get_config

if IS_SAVE_LOG := config["is_save_log"]:
	__new_log()

if __name__ == '__main__':
	if 1:
		print("this model won't execute without being imported as lib!")
		print("starting debug commandline")
		while True:
			try:
				exec(input("\n>>> "))
			except KeyboardInterrupt:
				if input("do you want to exit? (y/n):　") == 'y':
					exit()
			except SystemExit:
				sys.exit()
			except Exception as e:
				print(f"A Exception has occurred during the execution:\n{e}")
