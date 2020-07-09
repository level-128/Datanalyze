### this folder stores the required file and components for running the software. 

&nbsp;

#### 1. `config_library.py`

The `config_library.py` is a universal bottom layer. This layer is also used 
in [PythonLinearAlgebra](https://github.com/EPIC-WANG/PythonLinearAlgebra). 

it serves:

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

&nbsp;

#### 2. `run.py`

**you should ignore this file. this file is only used for rapid debugging**

&nbsp;

#### 3. `bootconfig.cfg`

this file saves the configuration of the software in JSON format. it is not 
recommend to delete this file. Although `bootconfig.cfg` will regenerate with
default value (hardcoded) when `config_library.py` detects that the file does
not exist, your user configuration (such as your axes information, DPI zoom, 
default format, linewidth ......) will be deleted. 

If this file is corrupt, the `config_library.py` will removes this file 
automatically and requires you to restart.

&nbsp;

#### 4. `import list.cfg`

read [README](https://github.com/EPIC-WANG/Datanalyze/blob/master/Lib/README.md)
under Lib for more info

&nbsp;

#### 5. `config_log.log`

this is a log file. to disable this, enter **'settings'** and uncheck the log
option at the bottom of the window. 
