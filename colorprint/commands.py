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
    field_form = re.compile(r'((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?')
    group_form = re.compile(r'(?:\+|-)?\d+')
    color_form = re.compile(r'(?!\d)\w*')

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


    def field2slice(match):
        if ':' in match.group():
            k = slice(*tuple(i and int(i) for i in match.groups()))
        else:
            i = int(match.group(1))
            if   i > 0:
                k = slice(i-1,  i,    None)
            elif i == 0:
                k = slice(None, None, None)
            elif i == -1:
                k = slice(-1,   None, None)
            else:
                k = slice(i,    i+1,  None)
        return k


    def patt2stage(cond):
        patt, cond_ = re.compile(cond[0]), cond[1:]

        gidc = []
        for idx, arg in enumerate(cond_):
            m = group_form.fullmatch(arg)
            if m:
                group_idx = int(m.group())
                if group_idx <= 0:
                    raise ValueError('group index should be greater than zero')
                gidc.append(group_idx)
            else:
                colors = cond_[idx:]
                break
        else:
            colors = ()
        if not gidc:
            gidc = [0]

        if any(color_form.fullmatch(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (patt, gidc, attr)


    def field2stage(cond):
        fields = []
        for idx, arg in enumerate(cond):
            m = field_form.fullmatch(arg)
            if m:
                fields.append(field2slice(m))
            else:
                colors = cond[idx:]
                break
        else:
            colors = ()

        if not fields:
            raise ValueError('should give at lease one field')

        if any(color_form.fullmatch(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (fields, attr)


    def trans2stage(cond):
        cls = cond[0].__class__.__name__
        if cls == 'patt_arg':
            r = patt2stage(cond)
        else:
            r = field2stage(cond)
        return r


    stages = tuple(map(trans2stage, namespace.conditions))
    return (stages, sep)


def gen_coloring_func(stages, sep):
    def coloring_func(orig_string):
        string = orig_string.rstrip('\r\n')
        line_feed = orig_string[len(string):]

        def gen_field_pos(finditer, last=0):
            try:
                m = next(finditer)
                s,e = m.start(), m.end()
                yield (last, s)
                yield from gen_field_pos(finditer, e)
            except:
                yield (e, len(string))


        def gen_pos_color(stages):
            if any(len(stage)==2 for stage in stages):
                L = tuple(gen_field_pos(sep.finditer(string)))
                I = tuple(range(len(L)))

            for stage in stages:
                if len(stage)==2:
                    fields, color = stage
                    for idx in set(sum((I[s] for s in fields),())):
                        start, end = L[idx]
                        yield (start, end, color)
                else:
                    patt, gnums, color = stage
                    m = patt.search(string)
                    for gn in gnums:
                        if gn <= len(m.groups()):
                            yield (m.start(gn), m.end(gn), color)


        def gen_slices(states):
            keys = list(states.keys())
            for z in zip([0]+keys, keys+[None]):
                yield slice(*z)


        def gen_attr(states):
            state = []
            for move in states.values():
                if move['add']:
                    state.extend(move['add'])
                for color in move['del']:
                    state.remove(color)
                yield sum(state,())


        def attr2ctrl(attr):
            return '\033[{}m'.format(';'.join(map(str, attr)))

        from collections import OrderedDict
        states = {}
        for start, end, color in gen_pos_color(stages):
            states.setdefault(start, {'add':[], 'del':[]})['add'].append(color)
            states.setdefault(end,   {'add':[], 'del':[]})['del'].append(color)
        states = OrderedDict(sorted(states.items(), key=lambda t:t[0]))
        print(states)

        colored_form = '{}'+'{}'.join(map(attr2ctrl, gen_attr(states)))+'{}'+line_feed
        return colored_form.format(*(string[s] for s in gen_slices(states)))


    return coloring_func


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
            stages, sep = get_stages(parser, namespace)
        except (ValueError, KeyError) as e:
            parser.error(e.args[0])

        func = gen_coloring_func(stages, sep)
        write = gen_coloring_write(func, namespace.not_redirect,
                                   stdout=sys.stdout, stderr=sys.stderr)
        for line in sys.stdin:
            write(line)
