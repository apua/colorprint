=================
VT100 Color Print
=================

The color print functions and command line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:version: 2
:author: Apua
:date: 2014.12 - 2015.02

`VT100 Color Print` is a tool for coloring output quickly.

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

For pythonic, it can color output with :code:`colors` parameter:

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

   colorprint --separator ',' --fields 1:3 red \
              --fields 1 3 5 -1 reverse < data.csv

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

Though `VT100 Color Print` provides `built-in color names`__,
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

   colorprint --color-names

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

- :Q: Why take the PyPI name so long?

  :A: I prefer to use "ColorPrint", but it has been taken.
      However, that's OK, I think the current name is explicit
      to show that "it supports VT100".

- :Q: Can`t it run on M$ Windows?

  :A: What is M$ Windows?

- :Q: Why don`t you just take the function name "print" as built-in?

  :A: It is for distinguishing original built-in function and new built one;
      in the other side, "print" is a statement in python2.x, and it would
      raise `SynxtaxError` when naming "print".

- :Q: Why do you design color names as attributes of `print_` function?

  :A: It is just for convenience.
      Please consider which is shorter and easy to add/remove color below:

      .. code-block:: Python

         # origin
         print(sep='\n', *range(10))
         # colored
         print.red.reverse(sep='\n', *range(10))
         print(sep='\n', colors=['red', 'reverse'], *range(10))

      Opposite, the function with argument `colors` is for explicit using.

- :Q: What is the purpose of the command-line tool?

  :A: It is designed as a light weight tool for coloring line by line.
      It is useful such as with `tail -f $LOG` or drawing some text temporarily.

      In most cases, for example, `git log` and `date`, are not appropriate colored line by line.
      Instead, they would provide `format` option to color easily.

- :Q: How about providing `--mode` option in command-line tool,
      which is used like `--mode=httpd` and `httpd` is work for some user defined pattern?
      It could increase *reusability*.

  :A: Since it is just a light weight tool, it is no need to consider reusability.

      To design `--mode` support is very difficult,
      because there are many new things should be considered.
      For example, the same color names might not have same display in different terminal emulater,
      and user might want to use different color names,
      however, there might be more than one pattern and more than one color,
      thus it is complicated to decide which pattern takes which color.

      Compare with reusability, making the tool flexible is more important.

- :Q: I think the color names are too verbose in shell.

  :A: You can define customized color names.

- :Q: I am confused what color names I definded and which color names are built-in.

  :A: There is a argument of command could show that.

- :Q: Why are there two ways to write custom definitions?

  :A: If user has less definitions, they can just be combined to one line, like `GREP_COLORS` or `PATH`.
      We consider "Flat is better than nested", we think it is no need to expand it as single file.

      However, if there are more definitions enough, we may consider "Sparse is better than dense",
      and want to collected it as a single file.

- :Q: I worry about typo in customization, and a mistake that taking both defining ways in the same time.

  :A: Definition parser follows three rules below:

      - The separator of a definition is semicolons and equal sign,
        but you can also use space, comma, vertical bar, and hyphen.

      - There should be colons between definitions in one line defining way.

      - The color name has to be lowercase, start with character, and contain only character/digit/underscore.

      Thus it should be easy to write and debug.

      When user takes both ways to define custom color names, "single file" will win, and we will warn user.
      After warning, one can use `colorprint` command to merge or remove configurations.

- :Q: I want to transfrom the color name defining way.

  :A: There is an argument of command to do it.

- :Q: I don`t care about beautiful colors or complex pattern matching,
      I want to focus on which fields I care about.

  :A: You can use `alias` or `function` which is according to your shell. For example:

      .. code:: Bash

         #!/bin/bash

         alias cpf='colorprint --fields'
         cpf 1 3 5 reverse

         cpfr () { cpf "$@" reverse ; }
         cpfr 1 3 5

         cppr () { colorprint --pattern "$@" underscore ; }
         cppu 'patt_1|patt_2'


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
================   ======

.. [0] A custom color name.


References
==========

- http://www.termsys.demon.co.uk/vtansi.htm#colors

- http://misc.flogisoft.com/bash/tip_colors_and_formatting


Special Thanks
==============

(In alphabetical order)

+ dv - https://github.com/wdv4758h/
+ iblis - https://github.com/iblis17/
+ pi314 - https://github.com/pi314/
+ su - https://github.com/u1240976/
