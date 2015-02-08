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


def get_stages(parser, namespace):
    import re
    from .attributes import color_attr_mapping

    sep = re.compile(namespace.separator)
    field_form = re.compile(r'^((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?$')
    group_form = re.compile(r'^(?:\+|-)?\d+$')
    color_form = re.compile(r'^(?!\d)\w*$')

    #color_help = parser._actions[-4].help
    #field_help = parser._actions[-3].help
    #patt_help  = parser._actions[-1].help

    def colors2attr(colors):
        if not colors:
            if not namespace.default:
                raise ValueError('it should be given at least one color')
            colors = namespace.default

        attr = ()
        for c in colors:
            try:
                _attr = color_attr_mapping[c]
            except KeyError as e:
                raise KeyError('color "{}" is not defined'.format(e.args[0]))
            attr += _attr
        return attr


    def patt2stage(cond):
        patt, cond_ = re.compile(cond[0]), cond[1:]

        gidc = set()
        for idx, arg in enumerate(cond_):
            m = group_form.match(arg)
            if m:
                group_idx = int(m.group())
                if group_idx <= 0:
                    raise ValueError('group index should be greater than zero')
                gidc.add(group_idx)
            else:
                colors = cond_[idx:]
                break
        else:
            colors = ()
        if not gidc:
            gidc.add(0)

        if any(color_form.match(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (patt, gidc, attr)


    def field2stage(cond):
        fields = set()
        for idx, arg in enumerate(cond):
            m = field_form.match(arg)
            if m:
                fields.add(tuple(i and int(i) for i in m.groups()))
            else:
                colors = cond[idx:]
                break
        else:
            colors = ()

        if not fields:
            raise ValueError('should give at lease one field')

        if any(color_form.match(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (fields, attr)

    def trans2stage(cond):
        cls = cond[0].__class__.__name__
        if cls == 'patt_arg':
            return patt2stage(cond)
        else:
            return field2stage(cond)

    stages = tuple(map(trans2stage, namespace.conditions))
    return (sep, stages)


def gen_coloring_func(sep, stages):
    return '\033[38;5;38m{}\033[m'.format


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

    parser = create_parser()
    namespace = parser.parse_args()

    if   namespace.show16 is not None:
        if namespace.show16:
            parser.exit(message=format_color(namespace.show16))
        else:
            parser.exit(message=format_color16())
    elif namespace.show256 is not None:
        if namespace.show256:
            parser.exit(message=format_color(namespace.show256))
        else:
            parser.exit(message=format_color256())
    else:
        if namespace.conditions is None:
            parser.print_help()
            parser.exit()
        try:
            sep, stages = get_stages(parser, namespace)
        except (ValueError, KeyError) as e:
            parser.error(e.args[0])

        func = gen_coloring_func(sep, stages)
        write = gen_coloring_write(func, namespace.not_redirect,
                                   stdout=sys.stdout, stderr=sys.stderr)
        for line in sys.stdin:
            write(line)
