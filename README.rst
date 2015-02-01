=================
VT100 Color Print
=================

:version: 2


`VT100 Color Print` is a tool for temporary colorful printing.

It is designed for convenience with intuitive color names,
and simple ways to quickly let the output string colorful.


Installation
============

``pip install vt100-colorprint``


Usage
=====

Run as command
--------------

Select fields to color::

    colorprint --fields 2::2 -1 yellow bggreen underscore

Choose specified separator::

    colorprint --fields 5 reverse --separator ', *'

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


Built in names
--------------

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
cyan               36
white              37
bgblack            40
bgred              41
bggreen            42
bgyellow           43
bgblue             44
bgmagenta          45
bgpurple [0]_      45
bgcyan             46
bgwhite            47
================   ======

.. [0] A custom color name.


FAQ
===

- :Q: Why take the PyPI name so long?

  :A: I prefer "ColorPrint" but it has been taken.
      That's OK, I think adding prefix would be more explicit that
      "it support VT100".

- :Q: Why create another colorful `print` function?

  :A: I need a simple and intuitive way to write a temporary code.
      What I found are not simple or intuitive enough.

- :Q: Why create another colorful output command?

  :A: I found there are many good command tool on PyPI, but not enough.
      They usually support only basic color, so that when one color shows
      not well on some terminal, it can not be given advanced set such as
      'bright', 'underscore', 'reverse'....etc.

- :Q: Why not consider `print` statement?

  :A: Print function is more powerful, useful.
      In addition, `print` statement takes keyword 'print', thus it is very
      difficult to design the tool.

- :Q: I think the command is too long....

  :A: Please use `alias` command in shell.

- :Q: The color names are too verbose in shell.

  :A: Explicit is better than implicit, it is not necessary to
      remember the abbreviation of color names;
      if it needs to record the repeatedly usedcolor combination,
      please consider add it to your environment setting in shell.

- :Q: Why provide a colorful string generator tool?

  :A: If you need colorful strings in your product,
      custome made is better, I think.


Reference
=========

- http://www.termsys.demon.co.uk/vtansi.htm#colors

- http://misc.flogisoft.com/bash/tip_colors_and_formatting
