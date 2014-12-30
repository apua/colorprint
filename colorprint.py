#! /usr/bin/env python3.4

"""
===================================
Color Print - VT100 Print Functions
===================================


When to use it
==============

When you develop a program, it might be helpful if you want to colorful print some data.

It is just designed for convenience and not a pythonic design, .

Usage
=====

1. To test effect on your terminal emulator, try::

       python3.4 -m colorprint

2. To enable colorful print functions, try::

       from colorprint import *

   Be careful of namespace.

   After imporing, you can set VT100 attribute with explicit name.

   For example, you can write::

       yellow.black.underscore.blink.print(data)

   And, the output equals ``'\x1b[33;40;4;5m{}\x1b[m'.format(data)``.

3. If you want to customize "name - attributes" mappings, you can create a dict in the forms:

   - `{ name: attr }`
   - `{ name: (attr1, attr2, ...) }`

   where `name` is type `str`, and `attr` is type `int`,
   and then use ``generate_functions`` and ``vars().update`` to generate functions and set them as global variables.

   Or, you can just update existed mappings::

       from colorprint import mapping, generate_functions
       mapping.update({'gray': (1,37)})
       functions = generate_functions(mapping)
       vars().update(functions)
       __all__ = tuple(functions.keys())
"""

__version__ = '1.0'
__author__ = 'Apua'


class VT100_Attributes(dict):
    """
    Generate attributes with VT100 attributes as default
    """

    _state = {
        'reset':      0,
        'bright':     1,
        'dim':        2,
        'underscore': 4,
        'blink':      5,
        'reverse':    7,
        'hidden':     8,
        }
    _foreground = {
        'black':     30,
        'red':       31,
        'green':     32,
        'yellow':    33,
        'blue':      34,
        'magenta':   35,
        'cyan':      36,
        'white':     37,
        }
    _background = {
        'bgblack':     40,
        'bgred':       41,
        'bggreen':     42,
        'bgyellow':    43,
        'bgblue':      44,
        'bgmagenta':   45,
        'bgcyan':      46,
        'bgwhite':     47,
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for k,v in (self._state.items()
                    |self._foreground.items()
                    |self._background.items()):
            self[k] = self.get(k, v)


def generate_functions(attrs):
    """
    Generate a `dict` containing {name: function}
    """

    class NewFunction:
        """
        The new colorful function class
        """

        def __init__(self, values):
            self.values = values

        def __getattribute__(self, name):
            attr = attrs.get(name)
            if attr is not None:
                if isinstance(attr, tuple):
                    return NewFunction(self.values+attr)
                else:
                    return NewFunction(self.values+(attr,))
            else:
                return super().__getattribute__(name)

        def print(self, *args, **kwargs):
            """The colorful print function"""
            coloring = '\x1b[' + ';'.join(map(str, self.values)) + 'm{}\x1b[m'
            print(*map(coloring.format, args), **kwargs)

    functions = {}
    for name, value in attrs.items():
        if isinstance(value, tuple):
            functions[name] = NewFunction(value)
        else:
            functions[name] = NewFunction((value,))
    return functions


Customized = {
    'light':      1,
    'underline':  4,
    'gray':       (1,37),
    'grey':       (1,37),
    'purple':     35,
    'bgpurple':   45,
    }

mapping = VT100_Attributes(Customized)
functions = generate_functions(mapping)
vars().update(functions)
__all__ = tuple(functions.keys())


if __name__=='__main__':
    for cate in ('_state','_foreground','_background'):
        for method, _ in sorted(vars(VT100_Attributes)[cate].items(),
                                key=lambda t:t[1]):
            #print(method, end=' ')
            vars()[method].print(method)
        print('-'*20)
    grey.bgpurple.underline.print('customized')
