"""
this library is a interpreter of the GUI, which serve to translate the mathematics language to the python command
and calling the plotting api in the yuyi

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
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Tuple, List, Union, Any
from config.config_library import get_config, set_config, printf, debug_log
import random


"""these are the constants which will be used in the parser."""

VAR_LIST = (
    'x', 'theta', 'y', 'z', 'r', 'I', 'e', 'pi', 'abs', 'factorial', 'sum', 'sin', 'cos', 'tan', 'log', 'ln', 'sinh', 'cosh', 'tanh',
    'arcsin', 'arccos', 'arctan', 'arcsinh', 'arccosh', 'arctanh', 'sinc', 'mod', 'floor', 'ceil', 'gcd', 'lcm', 'comb',
    'perm', 'conj', 'degrees', 'radians', 'exp')

VAR_DICT = dict()
for c in VAR_LIST: VAR_DICT[c[0]] = VAR_DICT[c[0]] + [c] if c[0] in VAR_DICT else [c]

CONSTANT_AND_VAR_LIST: tuple = ('x', 'y', 'z', 'r', 'I', 'e', 'pi', 'theta')

SIGNS_STR: tuple = ('+', '-', '*', '/', '^', '%', '=', '(', ')', '[', ']', '{', '}')

CONST_LEFT_PARENTHESIS: int = 1
CONST_RIGHT_PARENTHESIS: int = 2
CONST_CONSTANT: int = 3  # include numbers and variables
CONST_FUNCTION: int = 4
CONST_MINUS: int = 5
CONST_MULTIPLY: int = 6
CONST_SIGN: int = 7
CONST_EVAL: int = 8
CONST_SIGNS: tuple = (CONST_SIGN, CONST_MULTIPLY, CONST_MINUS, CONST_LEFT_PARENTHESIS, CONST_RIGHT_PARENTHESIS)

CONST_VECTOR_MODE: int = 20
CONST_2D_MODE: int = 21
CONST_3D_MODE: int = 22
CONST_POLAR_MODE: int = 23

"""
create a figure when this file is imported from the datanalyze env.
"""

if __name__ != '__main__':
    import yuyi

    current_plt = yuyi.falcon()


class RaisedReturn(Exception):
    """
    This Exception is used for exiting the given statement.
    """

    def __init__(self, *args):
        printf(f"Raised return triggered. {args=}", self_=self)
        self.args = args
        pass


@debug_log
def new_fig(*void):
    global current_plt
    del current_plt
    current_plt = yuyi.falcon()


@debug_log
def show(*void):
    current_plt.show()


@debug_log
def plot(input_str: str, python_mode: bool = False):
    interpret_to_falcon(input_str, python_mode)


@debug_log
def save(file_type=get_config("$default_save_format"), file_dir=None) -> str:
    if file_dir is None:
        file_dir = f'Saved Image\\figure{str(get_config("fig_number", 1))}'
    printf("save the file with " + file_type + ' in ' + file_dir)
    current_plt.export_fig(file_type, file_dir)
    set_config(fig_number=get_config("fig_number", 1) + 1)
    return f'{file_dir}.{str(file_type)}'


# noinspection PyUnresolvedReferences
@debug_log
def interpret_to_falcon(input_str: str, python_mode: bool = False) -> None:
    """
    this method is the main method which could turn math syntax into python syntax
    :param input_str: the input function
    :param python_mode: True means the input will be exec as a python code, while False
    means the input will be analyzed.
    :return: None
    """
    if python_mode:
        plot = yuyi.falcon()
        exec(input_str)
    else:
        try:
            input_str = input_str.lstrip()
            __interpret_is_key_word(input_str)
            type_const: int = __interpret_which_mode(input_str)
            if type_const == CONST_VECTOR_MODE:
                current_plt.plot_vectors(input_str)
                return None
            
            input_str = __analyze_function(input_str)
            if type_const == CONST_POLAR_MODE:
                raise Exception("the polar mode is still developing")
            elif type_const == CONST_3D_MODE:
                current_plt.plot_3d(input_str)
            elif type_const == CONST_2D_MODE:
                current_plt.plot_2d(input_str)

        except RaisedReturn:
            return None


def __interpret_is_key_word(input_str: str) -> None:
    if input_str == 'HOLDOFF':
        set_config(new_fig=True)
        raise RaisedReturn()
    elif input_str == 'HOLDON':
        set_config(new_fig=False)
        raise RaisedReturn()
    elif input_str == 'PUSH':
        show()
        raise RaisedReturn()
    elif input_str[:4] == 'SAVE':
        try:
            filetype = input_str[4:].lstrip().rstrip()
            if filetype == '':
                raise Exception("The file type is not valid!")
        except:
            filetype: str = get_config("$default_save_format")
        save(filetype)
        raise RaisedReturn()
    return None


def __interpret_which_mode(input_str: str) -> int:
    """
    decide which plotting mode should use.
    include: 2d, 3d, vector, polar
    :param input_str:
    :return: return the plot mode of the given input str.
    """
    if _ := (input_str.replace(' ', '')[:2]) == 'z=':  # a 3D plot MUST begin with z=
        return CONST_3D_MODE
    elif _ == 'r=':
        return CONST_POLAR_MODE
    elif input_str[0] == '[':  # a vector must begin with '['
        return CONST_VECTOR_MODE
    else:
        return CONST_2D_MODE


def __analyze_find_vars(input_str: str, start_index: int) -> Tuple[str, int, Union[int, None]]:
    """
    find the element in the str from VAR_DICT
    :param input_str: ~
    :return: the found element, next index, the category of the index.
    """
    content_str: str = ''  # the return element str

    for index, content in enumerate(input_str[start_index:]):
        content: str

        if content == ' ':  # ignore the whitespace
            continue

        #  match the index which should used in input_str
        index += start_index

        if content == "#":
            """
            return the element until another # occurs
            """
            number_of_ind: int = 1
            for element in input_str[index + 1:]:
                if element == "#":
                    number_of_ind += 1
                    break
                content_str += element

            return content_str, index + len(content_str) + number_of_ind, CONST_EVAL

        if content in SIGNS_STR:  # append the sign in the variable sign
            return content, index + 1, [CONST_MINUS, CONST_LEFT_PARENTHESIS, CONST_RIGHT_PARENTHESIS, CONST_MULTIPLY, CONST_SIGN][
                '-()*'.find(content)]

        if content.isdigit() or content == '.':  # if the content is a number
            for _ in input_str[index:]:
                if _.isdigit() or _ == '.':
                    content_str += _
                else:
                    break
            return content_str, index + len(content_str), CONST_CONSTANT

        if content in VAR_DICT.keys():
            return_element: str = ''  # make sure always return the longest variable. for example, sinh, which may be
            # recognized as sin and h
            for _ in VAR_DICT[content]:  # index all variables according to the capital letters
                if input_str[index:index + (__ := len(_))] == _:  # if the element matches the element in VAR_DICT
                    # __ = len(_)
                    if len(_) > len(return_element):
                        return_element = _
                        return_len = __  # or the returned length will become the longest in the dictionary.

            if return_element == '':
                raise SyntaxError(f"the variable in '{input_str}' is not defined. ")
            return return_element, index + return_len, [CONST_FUNCTION, CONST_CONSTANT][
                bool(' '.join(CONSTANT_AND_VAR_LIST).find(return_element) + 1)]

        else:
            raise SyntaxError(f"the variable in '{input_str}' is not defined. ")

    return '', len(input_str), None  # nothing matched.


@debug_log
def __combine_element_from_lists(x: List[str], y: List[str], index: int, is_right: bool = False) -> Tuple[list, list]:
    """
    operate two lists x and y and combine the element(s) at index 'index' to the content located at the left side or
    the right side.
    :param x: list 1
    :param y: list 2
    :param index: the operation index
    :param is_right: is combine to the right
    :return: a tuple contains two lists.
    """
    x[index + _], y[index + _] = ''.join([x.pop(index), x[index + (_ := (int(is_right) - 1))]][::(__ := (int(is_right) * 2 - 1))]), \
                                 ''.join([y.pop(index), y[index + _]][::__])
    return x, y


def __insert_element_from_list(var_element_category: List[str], var_element: List[str], index: int, content: str) -> Tuple[list, list]:
    assert content in (_ := ('*', '(', ')'))
    var_element_category.insert(index, [CONST_MULTIPLY, CONST_LEFT_PARENTHESIS, CONST_RIGHT_PARENTHESIS][_.index(content)])
    var_element.insert(index, content)
    return var_element_category, var_element


def __analyze_add_signs(var_element: list, var_element_category: list) -> Tuple[list, list]:
    x = var_element_category.copy()
    y = var_element.copy()
    adjust_index = 0
    for index, content in enumerate(var_element_category):
        content: int
        index += adjust_index
        if not index:
            continue  # skip when the index is 0

        if content == CONST_LEFT_PARENTHESIS:
            # this is same with:  x[index-1] != CONST_FUNCTION   and   x[index-1] not in CONST_SIGNS
            if x[index - 1] in (CONST_RIGHT_PARENTHESIS, CONST_CONSTANT):
                x, y = __insert_element_from_list(x, y, index, '*')
                adjust_index += 1

        elif content == CONST_CONSTANT:
            if x[index - 1] == CONST_FUNCTION:
                x, y = __insert_element_from_list(x, y, index, '(')
                x, y = __insert_element_from_list(x, y, index + 2, ')')
                adjust_index += 2

            elif (_ := x[index - 1]) == CONST_CONSTANT or _ == CONST_RIGHT_PARENTHESIS:
                x, y = __insert_element_from_list(x, y, index, '*')
                adjust_index += 1

        elif content == CONST_FUNCTION:
            if (_ := x[index - 1]) == CONST_FUNCTION:
                raise SyntaxError("nested functions are not accepted because of ambiguous meaning. If you want to express python functions, "
                                  "use Python mode or use # between functions.")
            elif _ == CONST_CONSTANT or _ == CONST_RIGHT_PARENTHESIS:
                x, y = __insert_element_from_list(x, y, index, '*')
                adjust_index += 1
    return x, y


@debug_log
def __analyze_function(input_str: str) -> str:
    """
    transfer the syntax from python to the math -- adding auto "*" sign between signed variables
    :param input_str: ~
    :return: the modified input str
    """
    var_element = []  # the variables and element which used in the input_str. it contains all the element (signs and
    # variables)
    var_element_category = []  # the category of the
    element_index: int = 0  # the count of the next index which will be analyzed.
    is_negative: bool = False  # is the current situation negative
    element_str: str  # the current var

    while True:
        element_str, element_index, element_content = __analyze_find_vars(input_str, element_index)
        if not element_content:
            break

        # save the negative sign.
        if element_content == CONST_MINUS and (var_element_category == [] or var_element_category[-1] in (CONST_SIGNS, CONST_FUNCTION)):
            is_negative = not is_negative
            continue

        if is_negative:
            var_element.append('-' + element_str)
            is_negative = False
        else:
            var_element.append(element_str)
        var_element_category.append(element_content)

    printf(f"{var_element=}, {var_element_category=}", self_=__analyze_function)
    var_element_category, var_element = __analyze_add_signs(var_element, var_element_category)
    input_str = ' ' + ' '.join(var_element) + ' '
    input_str = input_str.replace("^", "**")
    printf(f"{input_str=}", self_=__analyze_function)
    return input_str


if __name__ == '__main__':
    while True:
        try:
            print(__analyze_function(input(">>")))
        except Exception as e:
            print("ERROR:", e)
