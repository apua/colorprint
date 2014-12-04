=====================
VT100 Print Functions
=====================

This is a module which provides print functions with color defined in 
`VT100 Display Attributes`_ .

VT100 Display Attributes
------------------------

The information comes from http://www.termsys.demon.co.uk/vtansi.htm .

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

Examples
--------

The usage is designed for fun::

 .. code:: Python
    # original print function
    print
    # foreground black
    black.print
    # foreground light black
    black.light.print
    # foreground black, background yellow
    black.yellow.print
    # foreground light black, background yellow
    black.light.yellow.print
