'''
Provide `print_` and `pprint_` methods
'''

from .attributes import color_attr_mapping


def colorform(vt_attr):
    attrs = ';'.join(map(str, vt_attr))
    return '\x1b[{}m{{}}\x1b[m'.format(attrs)


class ColorPrint:
    def __init__(self, vt_attr=()):
        self.vt_attr = vt_attr

    def __call__(self, *values, sep=None, end=None, file=None, flush=None, **kwargs):
        try:
            invalid_key = next(k for k in kwargs if k!='colors')
            raise TypeError("'%s' is an invalid keyword argument for this function" % invalid_key)
        except StopIteration:
            pass

        if self.vt_attr and 'colors' in kwargs:
            raise TypeError('Do not set colors in both attributes and parameters way')
        elif self.vt_attr:
            coloring = colorform(self.vt_attr).format
            values_ = map(coloring, map(str, values))
        elif 'colors' in kwargs:
            vt_attr = sum((color_attr_mapping[k] for k in kwargs['colors']), ())
            coloring = colorform(vt_attr).format
            values_ = map(coloring, map(str, values))
        else:
            values_ = values

        locals_ = locals()
        kwargs_ = {key: locals_[key] for key in ('sep','end','file','flush') if locals_[key] is not None}

        return print(*values_, **kwargs_)

    def __getattr__(self, color_name):
        try:
            return self.__class__(self.vt_attr + color_attr_mapping[color_name])
        except KeyError as e:
            raise AttributeError('Color "%s" is not defined' % e.args[0])


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


print_  = ColorPrint()
pprint_ = ColorPPrint()
