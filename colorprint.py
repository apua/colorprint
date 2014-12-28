#! /usr/bin/env python3.4


"""
Usage::
    from colorprint import *

Execute ``python3.4 -m colorprint`` to get colorful output testing.

>>> gen_print(state=1, foreground=38,background=41)(1234567890)
\x1b[1;38;41m1234567890\x1b[m

original print function
>>> print(*range(10))

foreground
>>> red.print(*range(10))

foreground - state
>>> red.bright.print(*range(10))

foreground - state - background
>>> red.bright.blue.print(*range(10))

foreground - background
>>> red.blue.print(*range(10))

foreground - background - state
>>> red.blue.bright.print(*range(10))

state
>>> bright.print(*range(10))

state - foreground
>>> bright.red.print(*range(10))

state - foreground - background
>>> bright.red.blue.print(*range(10))
"""


States = {
    'reset':      0,
    'bright':     1,
    'dim':        2,
    'underscore': 4,
    'blink':      5,
    'reverse':    7,
    'hidden':     8,
    # customized
    'light':      1,
    }

Foregrounds = {
    'black':     30,
    'red':       31,
    'green':     32,
    'yellow':    33,
    'blue':      34,
    'magenta':   35,
    'cyan':      36,
    'white':     37,
    # customized
    'purple':    35,
    }

Backgrounds = {
    'black':     40,
    'red':       41,
    'green':     42,
    'yellow':    43,
    'blue':      44,
    'magenta':   45,
    'cyan':      46,
    'white':     47,
    # customized
    'purple':    45,
    }


__all__ = tuple(Foregrounds) + tuple(States)


def gen_print(*, state=0, foreground=37, background=40):
    template = '\x1b[{state};{foreground};{background}m{}\x1b[m'
    coloring = lambda obj, loc=locals(): template.format(obj, **loc)
    return (lambda *args, **kwargs: print(*map(coloring, args), **kwargs))


def gen_fcns(settings=None) -> 'sub fcns :: (name, lambda)':
    fcns = {}
    if settings==None:
        # choose function name in States then set 'state'
        # and, in Foreground then set 'foreground'
        # to `gen_fcns` and `gen_fcns` should return fcns
        for func_name, value in States.items():
            fcns[func_name] = lambda: None
            vars(fcns[func_name]).update(gen_fcns({'state': value}))
        for func_name, value in Foregrounds.items():
            fcns[func_name] = lambda: None
            vars(fcns[func_name]).update(gen_fcns({'foreground': value}))
        return fcns
    else:
        if 'state' not in settings:
            for func_name, value in States.items():
                fcns[func_name] = lambda: None
                vars(fcns[func_name]).update(gen_fcns(
                   dict(settings.items()|{'state': value}.items())
                   ))
        if 'foreground' not in settings:
            for func_name, value in Foregrounds.items():
                fcns[func_name] = lambda: None
                vars(fcns[func_name]).update(gen_fcns(
                    dict(settings.items()|{'foreground': value}.items())
                    ))
        if 'background' not in settings \
           and 'foreground' in settings:
            for func_name, value in Backgrounds.items():
                fcns[func_name] = lambda: None
                vars(fcns[func_name]).update(gen_fcns(
                    dict(settings.items()|{'background': value}.items())
                    ))
        fcns['print'] = gen_print(**settings)
        return fcns

    
vars().update(gen_fcns())


if __name__=='__main__':

    for k in States:
        vars()[k].print('{:20}'.format(k), *range(10))
    for k in Foregrounds:
        vars(bright)[k].print('{:20}'.format(k), *range(10))
    for k in Backgrounds:
        vars(bright.white)[k].print('{:20}'.format(k), *range(10))

    print()
    gen_print(state=1, foreground=38,background=41)(*range(10))

    print()
    bright.black.print('original', end=' - ') ; print(*range(10))
    bright.black.print('F       ', end=' - ') ; red.print(*range(10))
    bright.black.print('F-S     ', end=' - ') ; red.bright.print(*range(10))
    bright.black.print('F-S-B   ', end=' - ') ; red.bright.blue.print(*range(10))
    bright.black.print('F-B     ', end=' - ') ; red.blue.print(*range(10))
    bright.black.print('F-B-S   ', end=' - ') ; red.blue.bright.print(*range(10))
    bright.black.print('S       ', end=' - ') ; bright.print(*range(10))
    bright.black.print('S-F     ', end=' - ') ; bright.red.print(*range(10))
    bright.black.print('S-F-B   ', end=' - ') ; bright.red.blue.print(*range(10))
