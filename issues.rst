`<http://www.google.com>`_

.. role:: strike
   :class: done
   
:strike:`qwer`

Issues
======

Python2 support
    [ ] python2 support with setuptools

command implement
    [ ] write help info to CLI tool
    [ ] add argument `--show-names`

methods implement
    [ ] let `print` be function but class instance

color_mapping implement
    [ ] given basic mapping at the beginning
    [ ] get custom definition when excuting `__getitem__`

`README.rst` implement
    [ ] FAQ :cmd:`echo ccc--ooo-----tt | python3.4 -m colorprint  -P "(--)" reverse`
    [ ] convenient tool
        - print.red.bgblue
        - check and set color
        - stream coloring

generate data from `README.rst`
    [ ] `author`/`version`
    [ ] :mod:`__init__` (doctest)
    [ ] `setup.py`

docstring (include part of doctest)
    [ ] :func:`color_mapping.defs2map`
    [ ] :func:`color_mapping.ColorMapping`
    [ ] :mod:`command`
    [ ] `README.rst`

unittest (in new style)
    [ ] :func:`methods.print`
    [ ] :func:`methods.pprint`
    [ ] :func:`color_mapping.defs2map`
    [ ] :mod:`commad` (undecided)

exception
    [ ] review error handler; 自訂顏色的檢查足夠嗎?
    [ ] :mod: `methods` exception messages
    [ ] use "During handling of the above exception, another exception occurred"
        or not?? consider :mod:`methods` line 48

naming and architecture
    [✓] `commands.run_cmd` → `command.run`
    [✓] `attributes.color_attr_mapping` → `color_mapping.colormap`
    [ ] refactor
    [ ] removing tail space
