import io
import pprint as pprint_module
import re

from .color_mapping import colormap

_print = print
_pprint = pprint_module.pprint


def identity(x):
    return x


def colorform(vt_attr):
    attrs = ';'.join(map(str, vt_attr))
    return '\x1b[{}m{{}}\x1b[m'.format(attrs)


class ColorPrint:
    """
    A new print function, which supports color name as attributes.
    The usage is same as built-in print function.
    """
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
        elif 'colors' in kwargs:
            vt_attr = sum((colormap[k] for k in kwargs['colors']), ())
            coloring = colorform(vt_attr).format
        else:
            coloring = identity

        values_ = map(coloring, map(str, values))
        locals_ = locals()
        kwargs_ = {key: locals_[key] for key in ('sep','end','file','flush') if locals_[key] is not None}

        return _print(*values_, **kwargs_)

    def __getattr__(self, color_name):
        try:
            return self.__class__(self.vt_attr + colormap[color_name])
        except KeyError as e:
            raise AttributeError('Color "%s" is not defined' % e.args[0])


class ColorPprint(ColorPrint):
    """
    A new pprint function, which supports color name as attributes.
    The usage is same as `pprint.pprint` function.
    """
    def __call__(self, values, stream=None, indent=1, width=80, depth=None, *, compact=False, **kwargs):
        """copy from `pprint.pprint`"""
        class ColoringTextIOWrapper(io.TextIOWrapper):
            def __init__(self, *a, coloring=identity, **kw):
                super().__init__(*a, **kw)
                self.patt = re.compile(r'^(,?)(\n\ *)(.*)$')
                self.coloring = coloring

            def write(self, s):
                m = self.patt.match(s)
                if m is not None:
                    a, b, c = m.groups()
                    colored = (a and self.coloring(a)) + b + (c and self.coloring(c))
                else:
                    colored = self.coloring(s)

                if isinstance(self.buffer, io.BufferedWriter):
                    write = super().write
                else:
                    write = self.buffer.write

                return write(colored)

            # Re-define behavior of :method:`close`,
            # since PrettyPrinter object will be destroyed after return,
            # and the wrappered stream would be deleted (and, closed) together.
            def close(self):
                if self.buffer is not None and not self.closed:
                    try:
                        self.flush()
                    finally:
                        #self.buffer.close()
                        pass

        try:
            invalid_key = next(k for k in kwargs if k!='colors')
            raise TypeError("'%s' is an invalid keyword argument for this function" % invalid_key)
        except StopIteration:
            pass

        if self.vt_attr and 'colors' in kwargs:
            raise TypeError('Do not set colors in both attributes and parameters way')
        elif self.vt_attr:
            coloring = colorform(self.vt_attr).format
        elif 'colors' in kwargs:
            vt_attr = sum((colormap[k] for k in kwargs['colors']), ())
            coloring = colorform(vt_attr).format
        else:
            coloring = identity

        printer = pprint_module.PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth, compact=compact)

        # Some class such as `io.StringIO` has no `buffer` attribute
        # and it is no need to encode/decode
        # see :module:`_pyio.py`
        if isinstance(printer._stream, io.BufferedWriter):
            printer._stream = ColoringTextIOWrapper(printer._stream.buffer, coloring=coloring)
        else:
            printer._stream = ColoringTextIOWrapper(printer._stream, coloring=coloring)

        return printer.pprint(values)


print = ColorPrint()
pprint = ColorPprint()
