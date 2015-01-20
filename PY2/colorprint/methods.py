"""
Provide `print` and `pprint` methods.
"""

from __future__ import print_function

from .attributes import attr_names


def colorform(values):
    attrs = ';'.join(map(str, values))
    return '\033[{}m{{}}\033[m'.format(attrs)


class ColorPrint:
    _print  = print

    def __init__(self, values=()):
        self.values = values

    def __call__(self, *args, **kwargs):
        colored = colorform(self.values).format
        outputs = map(colored, map(str, args))
        self._print(*outputs, **kwargs)

    def __getattr__(self, attr):
        values = attr_names.get(attr)
        if values is None:
            raise AttributeError('Color "%s" is not defined'%attr)
        return self.__class__(self.values+values)


class ColorPPrint(ColorPrint):
    def __call__(self, object, stream=None, indent=1, width=80, depth=None):
        """copy from `pprint.pprint`"""
        from pprint import PrettyPrinter
        import re

        printer = PrettyPrinter(stream=stream, indent=indent,
                                width=width, depth=depth)
        stream  = printer._stream
        color_stream = type('',(),{})()
        printer._stream = color_stream

        colored = colorform(self.values).format
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
