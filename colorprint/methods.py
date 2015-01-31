"""
Provide `print` and `pprint` methods.
"""

from .attributes import color_attr_mapping


def colorform(vt_attr):
    attrs = ';'.join(map(str, vt_attr))
    return '\033[{}m{{}}\033[m'.format(attrs)


class ColorPrint:
    _print  = print

    def __init__(self, vt_attr=()):
        self.vt_attr = vt_attr

    def __call__(self, *args, **kwargs):
        colored = colorform(self.vt_attr).format
        outputs = map(colored, map(str, args))
        self._print(*outputs, **kwargs)

    def __getattr__(self, color_name):
        vt_attr = color_attr_mapping.get(color_name)
        if vt_attr is None:
            raise AttributeError('Color "%s" is not defined' % vt_attr)
        return self.__class__(self.vt_attr + vt_attr)


class ColorPPrint(ColorPrint):
    def __call__(self, object, stream=None, indent=1, width=80, depth=None, *,
                 compact=False):
        """copy from `pprint.pprint`"""
        from pprint import PrettyPrinter
        import re

        printer = PrettyPrinter(stream=stream, indent=indent,
                                width=width, depth=depth, compact=compact)
        stream  = printer._stream
        color_stream = type('',(),{})()
        printer._stream = color_stream

        colored = colorform(self.vt_attr).format
        #color_stream.write = lambda s: stream.write(colored(s))
        def write(s, patt=re.compile(r'^(,?)(\n\ *)(.*)$')):
            m = patt.match(s)
            if m is not None:
                a, b, c = m.groups()
                stream.write((a and colored(a)) + b + (c and colored(c)))
            else:
                stream.write(colored(s))
        color_stream.write = write
        printer.pprint(object)


print  = ColorPrint()
pprint = ColorPPrint()
