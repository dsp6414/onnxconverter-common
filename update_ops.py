# -*- coding: utf-8 -*-
# The codegen script to build oopb opset functions

from onnxconverter_common import onnx_ops

OPTIONAL_ARG_BEGIN = 5
OPTIONAL_ARG_OMIT = 1


def str_func_kwarg(func_obj):
    lst_covars = func_obj.__code__.co_varnames[OPTIONAL_ARG_BEGIN:]
    lst_defaults = func_obj.__defaults__[OPTIONAL_ARG_OMIT:]
    output = ''
    for covar, val in zip(lst_covars, lst_defaults):
        def_val = str(val)
        if isinstance(val, str):
            def_val = '\'' + def_val + '\''
        output += ", {}={}".format(covar, def_val)
    return output


def str_pair_kwarg(func_obj):
    code_obj = func_obj.__code__
    lst_covars = code_obj.co_varnames[OPTIONAL_ARG_BEGIN:code_obj.co_argcount]
    output = ''
    for covar in lst_covars:
        output += ", {}={}".format(covar, covar)

    return output


def format_line(line):
    return line


def gen_apply_func(name, func_obj):
    output = "\n"
    output += "\t def {}(self, inputs, name=None, outputs=None{}):\n".format(name[6:], str_func_kwarg(func_obj))
    output += "\t\treturn self.apply_op(onnx_ops.{}, inputs, name, outputs{})".format(name, str_pair_kwarg(func_obj))
    return output


print(
    """
    # !!!!CODE-AUTOGEN!!!! #
    # The following code was generated by update_ops.py, please copy/paste from the output of it.""")

apply_fx = {v1: v2 for v1, v2 in onnx_ops.__dict__.items() if v1.startswith('apply_')}

for v1, v2 in apply_fx.items():
    code_obj = v2.__code__
    stardard_args = ('container', 'operator_name')
    args = code_obj.co_varnames[3:3+len(stardard_args)]
    if tuple(args) == stardard_args:
        print(gen_apply_func(v1, v2))
