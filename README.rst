================
VT100-ColorPrint
================

The color print functions and command line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Version:   2
:Author:    Apua
:Copyright: WTFPL
:Date:      2014.12 - 2015.02
:Url:       https://github.com/apua/colorprint

:Credits:
    `dv <https://github.com/wdv4758h/>`_,
    `iblis <https://github.com/iblis17/>`_,
    `pi314 <https://github.com/pi314/>`_,
    `su <https://github.com/u1240976/>`_
    (in alphabetical order)

:Downloads:
    .. image:: https://img.shields.io/pypi/dm/VT100-ColorPrint.svg
        :target: https://pypi.python.org/pypi/VT100-ColorPrint/
        :alt: Downloads


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
--------

There are provided the functions :code:`print_` and :code:`pprint_`
which work like built-in functions :code:`print` and :code:`pprint`.

with attributes
```````````````

You can call the color names as their attributes (i.e. members)
to get colorful output quickly:

.. code:: Python

   >>> from colorprint import print_ as print, pprint_ as pprint
   >>> print.reverse.underscore('abc', 123)
   [7;4mabc[m [7;4m123[m
   >>> pprint.reverse(dict(zip(range(3), 'abc')), depth=1)
   [7m{0: 'a', 1: 'b', 2: 'c'}[m

with parameters
```````````````

For pythonic, it can color output with parameter :code:`colors`:

.. code:: Python

   >>> colors = ['reverse', 'underscore']
   >>> print(colors=colors, *range(3))
   [7;4m0[m [7;4m1[m [7;4m2[m

mix colors
``````````

.. code:: Python

   >>> from colorprint import print_ as print
   >>> from colorprint import color_attr_mapping
   >>> color_attr_mapping['ocean'] = color_attr_mapping['bright'] + (38,5,27)
   >>> color_attr_mapping['ocean']
   (1, 38, 5, 27)
   >>> print.ocean('abc', 123)
   [1;38;5;27mabc[m [1;38;5;27m123[m

If there is mixed color used frequently,
you can set it to environment attribute.
See `Customization`_ section below.

Command
-------

There is a command :code:`colorprint` for coloring streaming data.
You can use it to color data line by line.

with fields
```````````

In basic, you can just select which fields to color
and which colors to use:

.. code-block:: Sh

   tail -f log | colorprint --fields 1 3 5 bright yellow

You can also choose fields with slicing:

.. code-block:: Sh

   colorprint --fields 1:3 red --separator ',' < data.csv

Or, choose the last field since unkown how many fields of given data:

.. code-block:: Sh

   colorprint --fields -1 reverse --separator ',' < data.csv

At the end, you can take multi actions in the same time.

.. code-block:: Sh

   colorprint --separator ',' --fields 1:3 red --fields 1 3 5 -1 reverse < data.csv

Attention, the number of field works as AWK field number
when greater than zero, and works as Python index or slice
in otherwise.

with pattern
````````````

You can find strings to color with regular expression.
It would color every matching strings:

.. code-block:: Sh

   cat log | colorprint --pattern '\[\d+\]' bright blue

In addition, it supports group numbers, so that you can
color only parts of given pattern:

.. code-block:: Sh

   cat log | colorprint --pattern '\[(\d+)\]' 1 bright blue

short arguments
```````````````

:code:`colorprint` provides short arguments for convenience.

=============   ==============
long argument   short argument
=============   ==============
`--fields`      `-F`
`--separator`   `-S`
`--pattern`     `-P`
=============   ==============

Customization
-------------

set color names
```````````````

Though `VT100-ColorPrint` provides `built-in color names`__,
you could customized color names by setting
environment variable :code:`COLORPRINT_CUSTOM`:

__ `The Built-in Color Names`_

.. code-block:: Sh

   export COLORPRINT_CUSTOM='grey=1,30 blueviolet=38,5,57'

If there are many definitions, you can write it in multiple lines
to get more readibility:

.. code-block:: Sh

   export COLORPRINT_CUSTOM='
        grey = 1, 30
        blueviolet = 38, 5, 57
        '

After customization, please check color names by excuting command below:

.. code-block:: Sh

   colorprint --show-names

find favorite colors
````````````````````

The arguments of command :code:`colorprint`,
:code:`--show16` and :code:`--show256`,
could show all colors.

In addition, you can test mixed colors quickly as below:

.. code-block:: Sh

   colorprint --show bright 38 5 57

customize command
`````````````````

Shell (such as Bourne Shell, Bash, ...etc) provides :code:`alias`,
:code:`function`, and :code:`variable`.
You can use these features to customize commmands.

Here are some examples with Bourne Shell:

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

- :Q: The name `VT100-ColorPrint` is verbose. Why not use shorter name, such as `ColorPrint`?
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

- :Q: I think the command name "colorprint" is too long, and I don`t like set color every time....
  :A: There should be :code:`alias` command or feature in your shell. Use it.

- :Q: The parameters are too flexible. I only have few use cases.
  :A: Please consider :code:`function` feature in your shell.


About customizing color:

- :Q: I am not sure if my customization works or not.
  :A: Use the command :code:`colorprint --show-names` to test it.

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
