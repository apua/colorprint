=================
VT100 Color Print
=================

:version: 2
:author: Apua


`VT100 Color Print` is a tool for coloring output quickly.

It provides:

1. A system command: :code:`colorprint`

2. Two functions: :code:`print` and :code:`pprint`

3. Flexibility of custome defined color name and default color.


Installation
============

:code:`pip install vt100-colorprint`


Usage
=====

Functions
---------

There are provided the functinos :code:`print` and :code:`pprint`.
They work like built-in :code:`print` and :code:`pprint`, but you can
quickly call the color names as their attributes, so that
you can get colorful output very soon:

.. code:: Python

   from __future__ import print_function # for Python2.x

   from colorprint import print, pprint
   print.bright.underscore.green.bgyellow(*range(100))
   pprint.reverse(dict(zip(range(3), 'abc')))

These functions are designed for temporary use.
It is not recommended that using them in production.

Commands
--------

Customizations
--------------

The built-in color names are show below - `The Built-in Color Names`_

You can also define customized color names
to environment variable  `COLORPRINT_CUSTOM`, like so:

.. code:: Sh

   COLORPRINT_CUSTOM='grey:(1,30), blueviolet:(38,5,57), \bgblueviolet

    # format: name values
    # eg: ESC[1;30m
    grey = 1 30
    # eg: ESC[38;5;57m which is 256 color foreground
    blueviolet = 38 5 57
    # eg: ESC[48;5;57m which is 256 color background
    bgblueviolet = 48 5 57
    # eg: ESC[4;1;32;48;5;57m
    highlight = underscore bold green bgblueviolet




Run as command
--------------

Select fields to color:

    :code:`colorprint --fields 2::2 -1 yellow bggreen underscore`

Choose specified separator:

    :code:`colorprint --fields 5 reverse --separator ', *'`

Search pattern to color::

    colorprint --pattern '(?sx) (\[)(\d+)(?(1)]).*(\2)' 2 3 reverse

If environment variable `COLORPRINT_DEFAULT` has been set,
it would be used as the default color when not specify color::

    # For Sh/Bash/Zsh ; in Csh/Tcsh, use ``setenv``
    export COLORPRINT_DEFAULT='bright white bgblue'
    colorprint --pattern '\d+' --fields 4

Or, you can specify default color with argument::

    colorprint --pattern '\d+' --fields 4 --default bright yellow bgblue

Shell is powerful enough.
If you want type less, consider `alias` command to cut command::

    alias pcf='colorprint --fields'

Or, you can set arguments as variable::

    match_number='\d+ reverse'

In addition, you can use every redirection feature to input file::

    pcf 3 $match_number < $input_file_name

By default, `colorprint` will delivery color information through shell redirection;
if you only want colorfully print on terminal but redirect plain text, here is::

    pcf 3 --not-redirect > $output_file_name

All arguments have short forms for convenience:

    ==================   ==============
    long argument        short argument
    ==================   ==============
    ``--fields``         ``-F``
    ``--separator``      ``-S``
    ``--pattern``        ``-P``
    ``--default``        ``-D``
    ==================   ==============


Use in developing program
-------------------------

You can import `colorprint` to get colorful print tools::

    from colorprint import print, pprint, colorlist

Then every color names after print function would let
printing string colorful::

    print.yellow.bgblue(sep='\n', *mylist)
    pprint.yellow.bgblue(mylist, depth=1)

Sepcial color needs can be defined::

   colorlist['grey'] = colorlist['yellow']+colorlist['bgblue']
   print.grey(mydata)

.. note::

   The methods are not designed Pythonic but just for convenience usage.
   It suggests not use it in production.

Define custom color names
-------------------------

You can set environment variable ``COLORPRINT_CUSTOM`` to indicate
which file contains custom color name.

The file content like so::

    # format: name values
    # eg: ESC[1;30m
    grey = 1 30
    # eg: ESC[38;5;57m which is 256 color foreground
    blueviolet = 38 5 57
    # eg: ESC[48;5;57m which is 256 color background
    bgblueviolet = 48 5 57
    # eg: ESC[4;1;32;48;5;57m
    highlight = underscore bold green bgblueviolet

You can run command to test terminal color support::

    colorprint --show16
    colorprint --show256

And, print the result of specified value::

    colorprint --show16 1 30
    colorprint --show256 48 5 57


FAQ
===

- :Q: Why take the PyPI name so long?

  :A: I prefer to use "ColorPrint", but it has been taken.
      However, that's OK, I think the current name is explicit
      to show that "it supports VT100".

- :Q: Can`t it run on M$ Windows?

  :A: What is M$ Windows?

- :Q: Why do you take the same `print` function name as built-in?

  :A: I want to color my output temporarily,
      so I want to use `print` function as usual and add/remove color quickly.

- :Q: Why do you design color names as attributes of `print` function?

  :A: It is just for convenience.
      Please consider which is shorter and easy to add/remove color below:

      .. code:: Python

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

        - The color name have to be lowercase, start with character, and contain only character/digit/underscore.

      Thus it should be easy to write and debug.

      When user takes both ways to define custom color names, "single file" will win, and we will warn user.
      After warning, one can use `Colorprint` command-line tool to merge or remove configurations.

- :Q: I want to transfrom the color name defining way.

  :A: There is an argument of command to do it.

- :Q: I don`t care about beautiful colors or complex pattern matching,
      I want to focus on which fields I care about.

  :A: You can use `alias` or `function` which is according to your shell. For example:

      .. code:: Bash

         #!/bin/bash

         alias cpf='colorprint --fields'
         cpf 1 3 5 reverse

         function cpfr { cpf "$@" reverse ; }
         cpfr 1 3 5

         funtcion cppr { colorprint --pattern "$@" underscore ; }
         cppu 'patt_1|patt_2'

.. 1. define color name
     1.1 (X) 考慮量多, 還是用單一檔案
     1.2 不考慮 COLORPRINT_XXX, 我定義的不是常數名稱, 所以不適合
     1.3 (X) 雖然考慮了 GREP_COLORS 的語法設計, 但量一多還是很難寫好看
     1.4 format 一切從簡; parser 會把 [,:;|\s]+ 全部換成空白, parsing 失敗會噴行號和 warning
     1.5 單一設定就會以 GREP_COLORS 的設計為主
     1.6 如果檔案和環境變數都有設定, 檔案優先, 噴 warning 說建議二選一
     1.7 容錯噴 warning; 除了環境變數一行設定以冒號分隔以外, 其他的都取代成空白
         print/pprint 也要在第一次 import 時提醒這個問題
     1.8 要有參數給出所有的參數和客製化參數

.. 2. default color
     2.1 no need to consider default color
         just set color explicit
     2.2 function cpf { colorprint --fields "$@" default_color ; }
     2.3 function cpp { colorprint --pattern "$@" default_color ; }
         stream | cpp patt | cpp patt

.. 3. 不考慮 `--mode` 因為
      這只是 light-weight tool, line by line, 僅能當作臨時上色用
      長期, 例如 date, 可以直接上色; git log 有上下文關係, 較不好上色
      所以就不考慮更偉大的使用方式
      但會提供 alias 和 function 的使用範例

.. 4. 追加 print/pprint 有參數 colors
      It is for explicit, so just use 'colors' as argument name


.. 5. 追加 兩種定義法的轉換, 它必須是互動式的功能


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
+ pi314 - https://github.com/pi314/
+ iblis - https://github.com/iblis17/
+ su - https://github.com/u1240976/
