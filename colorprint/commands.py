def create_parser():
    import argparse

    from .attributes import default_color
    from .info import __version__

    parser = argparse.ArgumentParser(
        prog='ColorPrint',
        description='...(give example and how conditions work)',
        epilog='...'*30,
        )
    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
        )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--show16', metavar='attr',
        nargs='*',
        type=int,
        help='==='*30,
        )
    group.add_argument(
        '--show256', metavar='attr',
        nargs='*',
        type=int,
        help='==='*30,
        )
    parser.add_argument(
        '--not-redirect',
        action='store_true',
        default=False,
        help='...'*30,
        )
    parser.add_argument(
        '-D', '--default', metavar='color',
        nargs='+',
        default=default_color,
        help='...'*30,
        )
    parser.add_argument(
        '-F', '--fields', metavar='condition',
        dest='conditions', nargs='+', action='append',
        type=type('field_arg',(str,),{}),
        help='...'*30,
        )
    parser.add_argument(
        '-S', '--separator', metavar='sep',
        default=r'\s+',
        help='...'*30,
        )
    parser.add_argument(
        '-P', '--pattern', metavar='condition',
        dest='conditions', nargs='+', action='append',
        type=type('patt_arg',(str,),{}),
        help='...'*30,
        )

    return parser


def get_terminal_size():
    "return (lines, cols)"
    import fcntl, struct, termios
    try:
        for fd in (0,1,2):
            v = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '*'*4))
            if v:
                return v
    except OSError:
        return (25, 80)


def attrs_output(vt_attrs):
    attrs  = ';'.join(map(str,vt_attrs))
    string = ' '.join(map(str,vt_attrs))
    return '\033[{}m{:8}\033[m'.format(attrs, string)


def format_color(vt_attrs):
    return attrs_output(vt_attrs)+'\n'


def format_color16():
    defined_numbers = sum(
        (tuple(range(*t)) for t in ((30,38),(40,48),(90,98),(100,108))),
        (0,1,2,4,5,7,8),
        )
    int2attrs = lambda i: (i,)
    vt_attrs_list = map(int2attrs, defined_numbers)
    strings = tuple(map(attrs_output, vt_attrs_list))
    options = '  '.join(strings[:7]) + '\n'
    foreground = '\n'.join('  '.join(strings[i:i+8]) for i in range(7,23,8))+'\n'
    background = '\n'.join('  '.join(strings[i:i+8]) for i in range(23,39,8))+'\n'
    return options + foreground + background


def format_color256():
    defined_numbers = tuple(range(256))
    int2attrs = lambda i: (38,5,i)
    vt_attrs_list = map(int2attrs, defined_numbers)
    strings = tuple(map(attrs_output, vt_attrs_list))
    return '\n'.join('  '.join(strings[i:i+8]) for i in range(0,256,8))+'\n'


def get_stages(namespace):
    return () # not lazy; break if failed


def gen_coloring_func(stages):
    return (lambda line: line)


def gen_coloring_write(func, not_redirect, stdout, stderr):
    if not_redirect:
        def write(line):
            stdout.write(line)
            stderr.write(func(line))
    else:
        def write(line):
            stdout.write(func(line))
    return write


def run_cmd():
    import sys
    from .attributes import color_attr_mapping

    parser = create_parser()
    ns = parser.parse_args()

    if   ns.show16 is not None:
        if ns.show16:
            parser.exit(message=format_color(ns.show16))
        else:
            parser.exit(message=format_color16())
    elif ns.show256 is not None:
        if ns.show256:
            parser.exit(message=format_color(ns.show256))
        else:
            parser.exit(message=format_color256())
    else:
        try:
            stages = get_stages(ns)
        except (ValueError, KeyError) as e:
            parser.error(e.message)

        func = gen_coloring_func(stages)
        write = gen_coloring_write(func, ns.not_redirect,
                                   stdout=sys.stdout, stderr=sys.stderr)
        for line in sys.stdin:
            write(line)
