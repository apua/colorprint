"""
Store color names and get custom names according to env
"""

import os


VAR_CUSTOM  = 'COLORPRINT_CUSTOM'
VAR_DEFAULT = 'COLORPRINT_DEFAULT'

basic_mapping = {
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
    'cyan':               (36,),
    'white':              (37,),
    'bgblack':            (40,),
    'bgred':              (41,),
    'bggreen':            (42,),
    'bgyellow':           (43,),
    'bgblue':             (44,),
    'bgmagenta':          (45,),
    'bgpurple':           (45,),
    'bgcyan':             (46,),
    'bgwhite':            (47,),
}


class AttributeMapping(dict):
    is_init = False
    custom_filename = ''

    @classmethod
    def retrieve_data(cls):
        if cls.custom_filename:
            pass
        return basic_mapping

    def update_if_not_init(self):
        cls = __class__
        orig_getattribute = object.__getattribute__
        if not cls.is_init:
            self_update = orig_getattribute(self, 'update')
            self_update(cls.retrieve_data())
            cls.is_init = True

    def __getattribute__(self, *a, **k):
        __class__.update_if_not_init(self)
        return object.__getattribute__(self, *a, **k)


AttributeMapping.custom_filename = os.environ.get(VAR_CUSTOM, '')
color_attr_mapping = AttributeMapping()

default_color = os.environ.get(VAR_DEFAULT, '')
