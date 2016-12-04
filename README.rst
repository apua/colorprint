*DEPRECATED: please consider https://github.com/jonathanslenders/python-prompt-toolkit*

================
VT100-ColorPrint
================

The color print functions and command line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Version:   2.0
:Author:    Apua
:Copyright: WTFPL
:Date:      2014.12 - 2015.05
:Url:       https://github.com/apua/colorprint

:Credits:
    `dv <https://github.com/wdv4758h/>`_,
    `iblis <https://github.com/iblis17/>`_,
    `pi314 <https://github.com/pi314/>`_,
    `su <https://github.com/u1240976/>`_
    (in alphabetical order)


`VT100-ColorPrint` is a tool for coloring output easily and quickly
without to remember `VT100 color attributes definitions`__.
It provides:

#. Two print functions: :code:`print_` and :code:`pprint_`.
#. A shell command: :code:`colorprint`.
#. Use the environment variable :code:`COLORPRINT_CUSTOM` to define color names.

__ `References`_


Installation
==============================

:code:`pip install vt100-colorprint`


Usage
==============================

The functions
--------------------

The package provides functions :code:`print_` and :code:`pprint_` which work like built-in functions :code:`print` and :code:`pprint`:

.. code:: Python

    >>> from colorprint import print_ as print, pprint_ as pprint

Member function
```````````````````

You can set color with member function as below:

.. code:: Python

    >>> print.reverse.underscore('abc', 123)
    [7;4mabc[m [7;4m123[m
    >>> pprint.reverse(dict(zip(range(3), 'abc')), depth=1)
    [7m{0: 'a', 1: 'b', 2: 'c'}[m

Parameter
```````````````````

You can alos set color with parameter :code:`colors`:

.. code:: Python

    >>> colors = ['reverse', 'underscore']
    >>> print(colors=colors, *range(3))
    [7;4m0[m [7;4m1[m [7;4m2[m

Customization
```````````````````

You can customize your favorite color and set a color name for convenience.

.. code:: Python

    >>> from colorprint import color_attr_mapping
    >>> color_attr_mapping['ocean'] = color_attr_mapping['bright'] + (38,5,27)
    >>> color_attr_mapping['ocean']
    (1, 38, 5, 27)
    >>> print.ocean('abc', 123)
    [1;38;5;27mabc[m [1;38;5;27m123[m


The shell command
--------------------

The command provides a shell command :code:`colorprint` coloring streaming data line by line:

.. code:: Sh

    colorprint --help

Fields
```````````````````

You can just select fields and color to highlight:

.. code:: Sh

    tail -f log | colorprint --fields 1 3 5 bright blue

In addition, you can choose fields with Python`s slice notation:

.. code:: Sh

    tail -f log | colorprint --fields 1:6:2 bright blue

You can also choose the last field like Python`s index notation while you don`t know how many fields:

.. code-block:: Sh

    tail -f log | colorprint --fields -1 bright blue

By default, the separator is regexp "\s+"; you can set othere separator such as ",":

.. code-block:: Sh

    colorprint --separator ',' --fields -1 bright blue < data.csv

.. note::

    The number of field works as AWK field number when greater than zero;
    otherwise, it works as Python`s index/slice notation.

Pattern
```````````````````

You can use regexp to find string to color:

.. code:: Sh

    tail -f log | colorprint --pattern '\[:\d+\]' bright blue

The command supports regexp group, so you can indicate which group you want to color:

.. code:: Sh

    tail -f log | colorprint --pattern '\[(\d+):(\d+)]' 1 2 bright blue

Short arguments
```````````````````

The command provides short arguments for convenience.

=============   ==============
long argument   short argument
=============   ==============
`--fields`      `-F`
`--separator`   `-S`
`--pattern`     `-P`
=============   ==============


Customization
--------------------

Set color
```````````````````

The package has `built-in color names`__, but you can set favorite color for frequent usage:

__ `The Built-in Color Names`_

.. code:: Sh

   export COLORPRINT_CUSTOM='grey=1,30 blueviolet=38,5,57'

It can be defined in multiple lines for more readibility:

.. code:: Sh

   export COLORPRINT_CUSTOM='
        grey = 1, 30
        blueviolet = 38, 5, 57
        '

The command has argument for checking custom color:

.. code-block:: Sh

   colorprint --show-names

Find color
```````````````````

The command has two arguments: :code:`--show16` and :code:`--show256`.
They will show all colors or given color attributes. You can use them to find your desire.

.. code:: Sh

   colorprint --show256 38 5 57

Customize command
```````````````````

Shell (such as Bourne Shell, Bash, ...etc) usually provides :code:`alias`, :code:`function`, and :code:`variable`.
You can use these features to customize commmands. Below are some examples:

- Since :code:`--fields` arguments always being used:

  .. code-block:: Sh

     alias cpf='colorprint --fields'
     cpf 1 3 5 reverse < file

- Since some colors always being used:

  .. code-block:: Sh

     cpfr () { colorprint --fields  "$@" reverse -S ',' ; }
     cpfr -1 < csv_file

- Since there are some highlight forms always being used:

  .. code-block:: Sh

     # "hl" stands for "highlight"
     export hlpid="--pattern '\[(\d+)\]' 1 reverse"
     export hldate="--pattern '(\d+):(\d+):(\d+)' 1 2 3 yellow"
     colorprint $hlpid $hldate < log


Frequently Asked Questions
==============================

About the package:

- :Q: The name `VT100-ColorPrint`_ is verbose. Why not use shorter name, such as `ColorPrint <https://pypi.python.org/pypi/colorprint/>`_?
  :A: Because it has been taken. See https://pypi.python.org/pypi/colorprint/

- :Q: Can it run on Microsoft Windows?
  :A: What is Microsoft Windows?

- :Q: I think the functinos (i.e. :code:`print_` and :code:`pprint_`) are useless for my production. 
  :A: Yes. These functions are just for temporary usage;
      defining your own coloring functions is better when you know which color you prefered.

- :Q: Is there a need to provide customizing color?
  :A: Yes. The display results are not all the same on different terminal emulaters.


About the funtions:

- :Q: Why not remove postfix of :code:`print_` and :code:`pprint_`?
  :A: It is for not confusing built-in :code:`print` and :code:`pprint`.

- :Q: Why there are two ways to set color on print function? What is the difference?
  :A: Setting color with parameter is more pythonic, and setting color with member function is more obvious.

- :Q: With member function, why do you put "print" at the start of line but the end?
  :A: We think it is more intuitive. Besides, it`s no effect between the two style with Vim.


About the command:

- :Q: I think the command name "colorprint" is too long, and the parameters are too flexible.
      I don`t like set color every time. I only have few use cases.
  :A: You can use shell features. Refer to `Customize command`_.


About customizing color:

- :Q: Why not provide a configuration file like :code:`~/.colorprint`?
  :A: *Flat is better than nested*, there is no need to write it in specified file since it is just used for defining colors.


The Built-in Color Names
==============================

================   ======
name               value
================   ======
reset              0
bold [0]_          1
bright             1
dim                2
underscore         4
underlined [0]_    4
blink              5
reverse            7
hidden             8
black              30
red                31
green              32
yellow             33
blue               34
magenta            35
purple [0]_        35
aqua [0]_          36
cyan               36
white              37
bgblack            40
bgred              41
bggreen            42
bgyellow           43
bgblue             44
bgmagenta          45
bgpurple [0]_      45
bgaqua [0]_        46
bgcyan             46
bgwhite            47
bgbblack           100
bgbred             101
bgbgreen           102
bgbyellow          103
bgbblue            104
bgbmagenta         105
bgbpurple [0]_     105
bgbaqua [0]_       106
bgbcyan            106
bgbwhite           107
================   ======

.. [0] A custom color name.


References
==============================

- `Display Attributes of ANSI/VT100 Terminal Control Escape Sequences <http://www.termsys.demon.co.uk/vtansi.htm#colors>`_

- `FLOZz' MISC » bash:tip_colors_and_formatting <http://misc.flogisoft.com/bash/tip_colors_and_formatting>`_

- `Colorex <https://bitbucket.org/linibou/colorex/wiki/Home>`_

- `Colored <https://pypi.python.org/pypi/colored>`_

- `Termcolor <https://pypi.python.org/pypi/termcolor>`_
