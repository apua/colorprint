"""
Provide `print` and `pprint` methods.
"""

from attributes import attr_names


def colorform(values):
    attrs = ';'.join(map(str, values))
    return '\033[{}m{{}}\033[m'.format(attrs)


class ColorPrint:
    _print  = print

    def __init__(self, values=()):
        self.values = values

    def __call__(self, *args, **kwargs):
        coloring = colorform(self.values).format
        outputs = map(coloring, map(str, args))
        self._print(*outputs, **kwargs)

    def __getattr__(self, attr):
        values = attr_names.get(attr)
        if values is None:
            raise AttributeError('Color "%s" is not defined'%attr)
        return self.__class__(self.values+values)


class ColorPPrint(ColorPrint):
    def __call__(self, object, stream=None, indent=1, width=80, depth=None, *,
                 compact=False):
        """copy from `pprint.pprint`"""
        from pprint import PrettyPrinter         

        printer = PrettyPrinter(stream=stream, indent=indent,
                                width=width, depth=depth, compact=compact)
        stream  = printer._stream
        colored_stream = type('',(),{})()
        printer._stream = colored_stream

        coloring = colorform(self.values).format
        colored_stream.write = lambda s: stream.write(coloring(s))
        printer.pprint(object)


print  = ColorPrint()
pprint = ColorPPrint()

if __name__=='__main__':
    pass

    # instantiate test
    #print(sep='\n', *N.items())
    #pprint(N)

    # method generating test
    #print(
    #    print.values, 
    #    print.red.values,
    #    print.red.bgcyan.values,
    #    sep='\n')

    # print function running test
    #print(' ', sep=' - ', *range(10)) 
    #print.red(' ', sep=' - ', *range(10))
    #print.red.bgcyan(' ', sep=' - ', *range(10))

    #N = 15
    #D = dict(zip(range(N),range(N)))
    #pprint(D)
    #pprint.red.bgcyan(D)

    # exception test
    #print.kkk

