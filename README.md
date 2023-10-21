# Datanalyze

![](https://img.shields.io/badge/branch-master-brightgreen.svg?style=flat-square)
![](https://img.shields.io/badge/version-20.07.09-blue.svg?style=flat-square)
![](https://img.shields.io/badge/readme_version-r20.07.10-yellow.svg?style=flat-square)
![](https://img.shields.io/badge/last_update-7/9/2020-violet.svg?style=flat-square)

Datanalyze is a mathematical graphing software, which uses Matplotlib as rendering 
back-end and equips an easy-to-use GUI.

Datanalyze supports to graph mathematical vectors and functions: it could handle either
explicit or implicit function in a polar or rectangular coordinate system, graphing 
them in 2D or 3D axes.

# This project is no longer maintained. 

------------------------------------------------------------------------------------

## Install

To install Datanalyze on Windows 10, download a 
[Windows installation package](https://github.com/EPIC-WANG/Datanalyze/releases/download/20.07.09/mysetup.exe) 
and complete the installation wizard. 

For MacOS and Linux users, Datanalyze **DOES NOT** officially support your platform. 
You should consider installing Windows, using [Wine](https://www.winehq.org/) or 
building your own Python environment (See [Datanalyze Python environment requirements
](https://github.com/EPIC-WANG/Datanalyze/blob/master/documents/Python%20Environment%20Requirements.md)).
There are no ongoing bug or coverage tests under these platforms, so GUI may
behave abnormal and some APIs may malfunction under Linux and MacOS

------------------------------------------------------------------------------------

## License

Copyleft (C) 2020 level-128

this software is licensed under _Unlicense_ license

This is free and unencumbered software released into the public domain.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>

------------------------------------------------------------------------------------

## Tutorial 

This tutorial will provides you an overview of what Datanalyze does. You only need
less than 5 minutes to complete the Tutorial, so please take a look.

For more information and advanced operations for Datanalyze, please go to 
[Datanalyze complete user guide](https://github.com/EPIC-WANG/Datanalyze/blob/master/documents/Datanalyze%20User%20Guide.md). 
This guide includes advanced Datanalyze commands and syntax as well as detailed 
settings which would customize your plot. 

---

&nbsp;

For windows platform, enter your installation folder, double click `Datanalyze.exe`
to run.

Then you will see this UI: 

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/basic%20frame.png)

To graph a equation, simply input your equation into the box and click `start new`

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/basic%20plot.png)

If you want to graph a equation on a existing figure instead of creating a new figure
, click `continue`.

---

&nbsp;

To adjust other settings, click `advanced mode` checkbox. The Main Frame will expand, 
which will also allow you to customize more parameters. 

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/full%20frame.png)

You can customize line colour, domain and range at the right part of the main frame.

Also, a friendly reminder, you can use __Python expressions__ in domain and range
settings, like this:

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/advanced%20plot_expression%20allow.png)

---

&nbsp;

If you want to graph more equations at once, make sure to write each equation in
a separate line. 

You can select different colours by pressing ctrl, different equation will use
a different colour that you have selected, listed from bottom to the end, before
creating the figure.

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/advanced%20plot.png) 

You can also use __Python expressions__ in the equation. To tell the parser that
you are using a Python expression instead of mathematical operations, use `#` 
to separate the expression. For instance, call a random generator and plot 
`#random.randint(-10,x)# = xy`

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/advanced%20plot%20python%20expression.png) 

---

&nbsp;

To graph polar equations, use `r` and `theta` instead of `y` and `x`:

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/basic%20plot%20polar.png)

Implicit polar equations are also supported in Datanalyze:

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/advanced%20plot%20polar.png)

`Left X axis` and `Right X axis` are used to adjust the domain of `theta` in polar 
mode. Adjusting the max `r` value display range, adjust the `Right Y axis` instead. 
`Left Y axis` takes no effect in polar mode.

---

&nbsp;

To graph 3D equations, make sure the equation start with `z = `. Datanalyze does
not support Implicit 3D equations. You can use your mouse to drag the frame.

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/3d%20plot.png)

To graph 2D or 3D vector, use square bracket to indicate vector(s), and use `;` to 
separate vector(s) and vectors' starting position(s).

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/2d%20vector%20plot.png)

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/3d%20vector%20plot.png)

---

&nbsp;

To indicate complex number, use a capital `I` instead. Datanalyze could graph
the real part of the equation and disregards the imaginary part.

To graph `y = x^I`:

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/complex%20number%20plot%20disregard%20imaginary.png)

The graph with imaginary part (red) looks like this:

![](https://github.com/EPIC-WANG/Datanalyze/raw/master/content/y%3Dx%5Ei%20plot.png)

---

&nbsp;

## Extra materials

### 1. File folder introduction

gives you an introduction about the folders provided with the environment.

1. [Lib](https://github.com/EPIC-WANG/Datanalyze/blob/master/Lib/README.md) 
under `Datanalyze\Lib`
2. [Saved Image](https://github.com/EPIC-WANG/Datanalyze/blob/master/Saved%20Image/README.md)
under `Datanalyze\Saved Image`
3. [config](https://github.com/EPIC-WANG/Datanalyze/blob/master/config/README.md)
under `Datanalyze\config`

### 2. Documents

1. [API Reference](https://github.com/EPIC-WANG/Datanalyze/blob/master/documents/API%20Reference.md), 
providing introductions about the APIs provided in Python mode
2. [Python Environment Requirements](https://github.com/EPIC-WANG/Datanalyze/blob/master/documents/Python%20Environment%20Requirements.md)
Guide for users who need to build an environment for debugging.

---

&nbsp;

## Contribute and bug fix

Welcome everyone to contribute. Simply using "pull request" to merge changes.

For bug fix, raise a issue and upload the log file (`config\cfg_log.log`). 
