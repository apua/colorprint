================
VT100-ColorPrint
================

The color print functions and command line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:version: 2
:author: Apua
:date: 2014.12 - 2015.02
:credis: In alphabetical order - 
         `dv <https://github.com/wdv4758h/>`_,
         `iblis <https://github.com/iblis17/>`_,
         `pi314 <https://github.com/pi314/>`_,
         `su <https://github.com/u1240976/>`_

`VT100-ColorPrint` is a tool for coloring output quickly without
remember `VT100 color attributes definitions`__.

__ `References`_

It provides:

1. A system command: :code:`colorprint`

2. Two functions: :code:`print_` and :code:`pprint_`

3. Flexibility of customing color.


Installation
============

:code:`pip install vt100-colorprint`


Usage
=====

Function
--------

There are provided the functions :code:`print_` and :code:`pprint_`
which work like built-in functions :code:`print` and :code:`pprint`.

with attributes
```````````````

You can call the color names as their attributes
to get colorful output quickly:

.. code-block:: Python

   from colorprint import print_ as print, pprint_ as pprint

   print.bright.underscore.green.bgyellow(*range(100))
   pprint.reverse(dict(zip(range(3), 'abc')), depth=1)

with parameters
```````````````

For pythonic, it can color output with parameter :code:`colors`:

.. code-block:: Python

   colors = ['bright', 'underscore', 'green', 'bgyellow']
   print(colors=colors, *range(100))

mix colors
``````````

.. code-block:: Python

   from colorprint import color_attr_mapping

   C['ocean'] = C['bright'] + (38,5,27)
   print(C['ocean']) # (1, 38, 5, 27)
   print.ocean(*range(10))

If there is mixed color used frequently,
you can set it as default.
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

set default colors
``````````````````

Though `VT100-ColorPrint` provides `built-in color names`__,
you could customized default color names by setting
environment variable :code:`COLORPRINT_CUSTOM`:

__ `The Built-in Color Names`_

.. code-block:: Sh

   export COLORPRINT_CUSTOM='grey=1,30 blueviolet=38,5,57'

If there are many definitions, you can write it in multiple lines
for getting more readibility:

.. code-block:: Sh

   export COLORPRINT_CUSTOM='
        grey = 1, 30
        blueviolet = 38, 5, 57
        '

After customization, please check the default color names
by excuting command below:

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


FAQ
===

- :Q: The name `VT100-ColorPrint` is verbose.
      Why not take `ColorPrint`?
  :A: Because it has been taken.
      See https://pypi.python.org/pypi/colorprint/0.1

- :Q: It seems like it cannot run on M$ Windows?
  :A: What is M$ Windows?

- :Q: About the functions :code:`print_` and :code:`pprint_`,
      I think it is not necessary to use it on product.
  :A: That`s right. These functions are used for colorful output
      temporary. It is useful when checking output.
      With the product code, it is recommended to define a function
      or assign variables for your special purpose.

- :Q: How about take "print" as the function name of :code:`print_`
      instead of "print\_"?
  :A: It should take different names between two different
      functions. And, Python2.x treats :code:`print` as statement,
      so that it is easy to make mistake with naming "print".

- :Q: Why does it provide functions with color attributes?
      Is it not enough that providing functions with parameter
      :code:`colors`?
  :A: Using attributes would be shorter and easy to edit.

- :Q: When writing with color attributes, why should we put "print"
      at the start of line but the end?
  :A: After discussion, we think it is intuitive to put it at
      the start of line.
      By the way, the editing speed of both are almost the same
      with Vim.

- :Q: Are the built-in 16 colors and background colors not enough?
  :A: No. The displays of colors on different terminal emulaters
      might be different, so it is necessary to provide
      customization ability.

- :Q: I am not sure if my customization works or not.
  :A: Try :code:`colorprint --show-names`.

- :Q: Does the customization work on the functions, too?
  :A: Yes.

- :Q: Why not provide a configuration file like
      :code:`~/.colorprint`?
  :A: It is only used to define colors.
      *Flat is better than nested*, there is no need to write it
      in specified file.


The Built-in Color Names
========================

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
==========

- `Display Attributes of ANSI/VT100 Terminal Control Escape Sequences <http://www.termsys.demon.co.uk/vtansi.htm#colors>`_

- `FLOZz' MISC » bash:tip_colors_and_formatting <http://misc.flogisoft.com/bash/tip_colors_and_formatting>`_

- `Colorex <https://bitbucket.org/linibou/colorex/wiki/Home>`_

- `Colored <https://pypi.python.org/pypi/colored>`_

- `Termcolor <https://pypi.python.org/pypi/termcolor>`_

