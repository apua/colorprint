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

You can easy to indicate and combine VT100 color attribute for coloring.
Here is an example to color whole string::

    colorprint --color light yellow bggreen underscore

Separate to Fields
~~~~~~~~~~~~~~~~~~

Color every parts of fields::

    colorprint split --color reverse

Indicate the seperator with regexp::

    colorprint split --field-seperator ',\s*' --color reverse

Indicate which fields would be colored::

    colorprint split --positions 1 3 5 --color reverse

More ways to indicate fields::

    colorprint split --positions 2:-1:2 -1 --color reverse

Set fields in different colors::

    colorprint split --map 2::2 bright red --map -1 reset cyan

Find with Regexp
~~~~~~~~~~~~~~~~

Find matched string to color::

    colorprint find --pattern '(?sx) (\[)(\d+)(?(1)]).*(\2)' 3 --color reverse

Set more than one matched pattern in different colors::

    colorprint find --map pam_unix red --map 'pam_unix\([^)]+)\)' blue


Shell suppport
~~~~~~~~~~~~~~

Abbreviation of color names::

    # Sh, Bash, Zsh, ...
    export grey='bright black'
    export gray=$grey

    # Csh, Tcsh, ...
    setenv grey='bright black'
    setenv gray=$grey

Default highlight color setting


Alias command name::

    # Sh, Bash, Zsh, ...
    alias pcf='colorprint field -P'

    # Csh, Tcsh, ...
    alias pcf colorprint field -P

Input file::

    pcf 3 < $input_file_name

Redirection with color information::

    pcf --always < $input_file_name > $output_file_name


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
