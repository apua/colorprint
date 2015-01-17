=================
VT100 Color Print
=================

:version: 2.0


`VT100 Color Print` is a tool for temporary colorful printing.

It might be helpful if you want to colorful print some data during developing program,
or reading data stream.

Be aware of `VT100 Color Print` is not designed Pythonic and do not use in your production.


Installation
============

``pip install vt100-colorprint``


Usage
=====


Color support test
------------------

Run as Python module::

    $ python -m colorprint

Run as a command::

    $ colorprint --test


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

    colorprint --pattern '\d+' --fields 4 --color bright yellow bgblue

If you define a custom name of colors in env, it can be use directly::

    # For Sh/Bash/Zsh ; in Csh/Tcsh, use ``setenv``
    export grey='bright black'
    colorprint --pattern '\d+' grey

Shell is powerful enough.
If you want type less, consider `alias` command to cut command::

    alias pcf='colorprint --fields'

Or, you can set arguments as variable::

    match_number='\d+ reverse'

In addition, you can use every redirection feature to input file::

    pcf 3 $match_number < $input_file_name

By default, `colorprint` will only colorfully print on terminal;
you can delivery color information through shell redirection with argument::

    pcf 3 --deliver > $output_file_name

All arguments have short forms for convenience:

    ===============   ==============
    long argument     short argument
    ===============   ==============
    ``--fields``      ``-F``
    ``--separator``   ``-S``
    ``--pattern``     ``-P``
    ``--color``       ``-C``
    ``--deliver``     ``-D``
    ===============   ==============


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


Appendix: VT100 Display Attributes
==================================

:source: http://www.termsys.demon.co.uk/vtansi.htm#colors

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
