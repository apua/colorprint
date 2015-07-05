import os
import re
import warnings

CUSTOM_VAR  = 'COLORPRINT_CUSTOM'

BASIC_MAPPING = {
    'reset':              (0,),
    'bold':               (1,),
    'bright':             (1,),
    'dim':                (2,),
    'underscore':         (4,),
    'underlined':         (4,),
    'blink':              (5,),
    'reverse':            (7,),
    'hidden':             (8,),
    'black':              (30,),
    'red':                (31,),
    'green':              (32,),
    'yellow':             (33,),
    'blue':               (34,),
    'magenta':            (35,),
    'purple':             (35,),
    'aqua':               (36,),
    'cyan':               (36,),
    'white':              (37,),
    'bgblack':            (40,),
    'bgred':              (41,),
    'bggreen':            (42,),
    'bgyellow':           (43,),
    'bgblue':             (44,),
    'bgmagenta':          (45,),
    'bgpurple':           (45,),
    'bgaqua':             (46,),
    'bgcyan':             (46,),
    'bgwhite':            (47,),
    }


def warn(message):
    import warnings
    warnings.warn(message, category=RuntimeWarning, stacklevel=2)


def defs2map(defs):
    r"""
    Transform definitions to mapping, and warn if there is wrong format or
    duplicate definitions.
    >>> M = {'grey': (1,30), 'blueviolet': (38,5,57)}
    >>> M == defs2map("grey=1,30 blueviolet=38,5,57")
    True
    >>> M == defs2map('''
    ...     grey = 1, 30
    ...     blueviolet = 38, 5, 57
    ...     ''')
    True
    """
    if not defs.strip():
        return {}

    form = re.compile('''
        (?P<sep>^|\s+)
        (?P<name>[_a-zA-Z]\w*)\s*
        =\s*
        (?P<attrs>[\ \t]*\d+([\ \t]*,[\ \t]*\d+)*,?)
        (?=\s|$)
        ''', re.X)
    duplicates = wformats = False #flags
    last = 0
    mapping = {}
    for m in form.finditer(defs.strip()):
        name = m.group('name')
        attrs = eval('('+m.group('attrs')+')')
        if name in mapping:
            duplicates = True
        if m.start()!=last:
            wformats = True
        mapping[name] = attrs
        last = m.end()
    if 'm' not in locals() or m.end()!=m.endpos:
        wformats = True

    if duplicates:
        warn("duplicate definition")
    if wformats:
        warn("wrong format definition")

    return mapping


#class ColorMapping(dict):
#    """
#    `ColorMapping` is a dict, will retrieve custom color name definitions
#    from environment variable `CUSTOM_VAR` when `__getitem__` has been called,
#    so that it avoids raising parsing custom data error when importing
#    `colorprint` module.
#    """
#    def __init__(self):
#        self.update(BASIC_MAPPING)
#        self._custom_defs = os.environ.get(CUSTOM_VAR)
#        self._retrieved = self._custom_defs is None
#
#    def __getitem__(self, key):
#        if not self._retrieved:
#            self.update(defs2map(self._custom_defs))
#            self._retrieved = True
#        return super().__getitem__(key)


colormap = BASIC_MAPPING.copy()
colormap.update(defs2map(os.environ.get(CUSTOM_VAR)))
#colormap = ColorMapping()
