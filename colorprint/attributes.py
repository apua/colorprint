"""
Store color names and get custom names according to env
"""

import os


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


def retrieve_custom_colors(custom_file):
    def warn(msg):
        import warnings
        return warnings.warn(msg, category=RuntimeWarning, stacklevel=3)

    # If file not exist, show warning
    # If parsing failed, show warning
    # If there is a custom name 'default', ignore and show warning
    try:
        #with
        '''
        Open file and parsing, then update `basic_mapping`
        If there is not such file or paring content failed, raise warning
        '''
        raise OSError
        return {}
    except OSError as e:
        warn('Cannot open custom color file "%s"' % e.filename)
        return {}
    except:
        warn('Parse custom color file failed')
        return {}


class AttributeMapping(dict):
    def __init__(self, custom_file):
        self.retrieved = False
        self.custom_file = custom_file

    def __getitem__(self, key):
        if not self.retrieved:
            self.update(BASIC_MAPPING)
            if self.custom_file:
                self.update(retrieve_custom_colors(self.custom_file))
            self.retrieved = True
        return super().__getitem__(key)


default_color = os.environ.get(VAR_DEFAULT, '')
custom_file = os.environ.get(VAR_CUSTOM, '')
color_attr_mapping = AttributeMapping(custom_file)
