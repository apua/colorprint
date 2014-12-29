===================================
Color Print - VT100 Print Functions
===================================

:version: 1.0

One can write explict color name for print function easily, like that::

    from colorprint import *
    yellow.bggreen.underscore.print(MyData)

If one wants use customized name for specific attributes, it can be updated like that::

    from colorprint import mapping, generate_functions
    vt100_attibutes.update({'gray': (1,37)})
    functions = generate_functions(vt100_attibutes)
    vars().update(functions)
    __all__ = tuple(functions.keys())
    
Thus one can customize own print functions as new module.

The display attributes and format are defined in http://www.termsys.demon.co.uk/vtansi.htm,
see `VT100 Display Attributes`_.


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
       vt100_attibutes.update({'gray': (1,37)})
       functions = generate_functions(vt100_attibutes)
       vars().update(functions)
       __all__ = tuple(functions.keys())


VT100 Display Attributes
------------------------

Set Attribute Mode::

    <ESC>[{attr1};...;{attrn}m

Sets multiple display attribute settings. The following lists standard attributes::

    0   Reset all attributes
    1   Bright
    2   Dim
    4   Underscore  
    5   Blink
    7   Reverse
    8   Hidden

        Foreground Colours
    30  Black
    31  Red
    32  Green
    33  Yellow
    34  Blue
    35  Magenta
    36  Cyan
    37  White

        Background Colours
    40  Black
    41  Red
    42  Green
    43  Yellow
    44  Blue
    45  Magenta
    46  Cyan
    47  White
