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
    parser.add_argument(
        '-D', '--default', metavar='color',
        nargs='+',
        default=default_color,
        help='...'*30,
        )
    parser.add_argument(
        '-N', '--not-redirect',
        action='store_true',
        default=False,
        help='...'*30,
        )
    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
        )

    subparsers = parser.add_subparsers(help='= =')
    subparser = subparsers.add_parser('show')
    group = subparser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-16', metavar='attr',
        dest='show_16', nargs='*',
        type=int,
        help='==='*30,
        )
    group.add_argument(
        '-256', metavar='attr',
        dest='show_256', nargs='*',
        type=int,
        help='==='*30,
        )

    return parser


def show_color(mode, attrs):
    pass


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
    #print(ns)
    #print(dir(parser))
    #print(parser.format_usage())

    def cmd_error(msg, parser=parser):
        prog = parser.prog
        templ = '{prog}: error: {msg}\n'
        sys.stderr.write(parser.format_usage())
        sys.stderr.write(templ.format(**locals()))
        sys.exit(2)

    #cmd_error('asdfghjkl;')

    if 'show_16' in ns:
        if ns.conditions is not None:
            cmd_error('don`t use commend and sub-commend together')

        if ns.show_16 is not None:
            show_color(16, ns.show_16)
        else:
            show_color(256, ns.show_256)
    else:
        try:
            stages = get_stages(ns)
        except (ValueError, KeyError) as e:
            cmd_error(e.message)

        func = gen_coloring_func(stages)
        write = gen_coloring_write(func, ns.not_redirect,
                                   stdout=sys.stdout, stderr=sys.stderr)
        for line in sys.stdin:
            write(line)
'''
try:

if '16' in ns:
    if ns.conditions is not None:
        parser.print_usage()

#
try:
    if ns.conditions:
        ns.conditions = tuple(map(be_strict, ns.conditions))
except ValueError as e:
    para, cond = e.args
    parser.print_usage()
    print("{}: error: invalid condition: {} {}".
          format(parser.prog, para, ' '.join(cond)))
except KeyError as e:
    color, = e.args
    parser.print_usage()
    print("{}: error: color {} is not defined".
          format(parser.prog, color))
return ns

def be_strict(cond):
    def get_type(arg):
        return str(arg.__class__).split("'")[-2].split('.')[-1]

    def be_field_args(cond):
        fields = set()
        colors = ()
        range_arg = re.compile(r'^([+\-\d]*):?([+\-\d]*):?([+\-\d]*)$')
        for idx, arg in enumerate(cond):
            m = range_arg.match(arg)
            if m is not None:
                fields.add(tuple(int(s) if s else None for s in m.groups()))
            else:
                colors = tuple(cond[idx:])
                break
        if not fields or any(c not in color_mapping for c in colors):
            raise ValueError('--field', cond)
        return {'func': color_by_field, 'fields': fields, 'colors': colors}

    def be_patten_args(cond):
        pattern = re.compile(cond[0])
        group_arg = re.compile(r'^(\d+)$')
        return {}

    if get_type(cond[0])=='field_arg':
        return be_field_args(cond)
    else:
        return be_patten_args(cond)
'''
