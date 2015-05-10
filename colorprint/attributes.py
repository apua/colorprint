"""
Store color names and get custom names according to env
"""

import os
import re


VAR_CUSTOM  = 'COLORPRINT_CUSTOM'
VAR_DEFAULT = 'COLORPRINT_DEFAULT'

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


def settings2attributes(settings):
    r"""
    Transform to attributes from settings.
    Also check duplicated keys.

    >>> f = lambda s: sorted(settings2attributes(s).items())
    >>> f('grey=1,30 blueviolet=38,5,57')
    [('blueviolet', (38, 5, 57)), ('grey', (1, 30))]
    >>> f('''
    ... grey = 1 , 30
    ... blueviolet = 38 , 5 , 57
    ... ''')
    [('blueviolet', (38, 5, 57)), ('grey', (1, 30))]
    >>> f('grey=1,30 kk blueviolet=38,5,57')
    [('blueviolet', (38, 5, 57)), ('grey', (1, 30))]
    >>> f('grey=1,30 grey=1,30 blueviolet=38,5,57')
    [('blueviolet', (38, 5, 57)), ('grey', (1, 30))]
    """
    def warn(message):
        import warnings
        warnings.warn(message, category=RuntimeWarning, stacklevel=3)

    def parse(parts):
        def split2tuple(string): return tuple(map(int, string.split(',')))
        kv_patt = re.compile(r'^(?P<key>[_a-zA-Z]\w*)=(?P<value>[\d,]+)$')

        attrs = []
        warns = []
        for idx, part in enumerate(parts):
            m = kv_patt.match(part)
            if m:
                attrs.append((m.group('key'), split2tuple(m.group('value'))))
            else:
                warns.append((idx+1, part))

        return tuple(attrs), tuple(warns)

    def find_dup(attrs):
        D = {}
        for k, v in attrs:
            D.setdefault(k, []).append(v)
        return tuple((k,vs) for k,vs in D.items() if len(vs)>1)

    merged = ' '.join(filter(None, map(str.strip, settings.splitlines())))
    space_cleaned = re.sub(r'\s*([=,])\s*', lambda m:m.group(1), merged)
    attributes, warn_parts = parse(space_cleaned.split())
    duplicate = find_dup(attributes)

    if warn_parts:
        hints = '\n'.join('    part {}: {}'.format(*part) for part in warn_parts)
        warn('failed parsing:\n' + hints)

    if duplicate:
        hints = '\n'.join('    key {}: {} | {}'.format(k, *vs) for k,vs in duplicate)
        warn('duplicated keys:\n' + hints)

    return dict(attributes)


class AttributeMapping(dict):
    def __init__(self, custom_settings):
        self.retrieved = False
        self.custom_settings = custom_settings

    def __getitem__(self, key):
        if not self.retrieved:
            self.update(BASIC_MAPPING)
            if self.custom_settings:
                self.update(settings2attributes(self.custom_settings))
            self.retrieved = True
        return super().__getitem__(key)


custom_settings = os.environ.get(VAR_CUSTOM, '')
color_attr_mapping = AttributeMapping(custom_settings)
