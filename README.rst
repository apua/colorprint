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

  :A: Please use `alias` statement in shell.

- :Q: The color names are too verbose in shell.

  :A: Explicit is better than implicit, it is not necessary to
      remember the abbreviation of color names;
      if it needs to record the repeatedly usedcolor combination,
      please consider add it to your environment setting in shell.


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
