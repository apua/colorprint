def get_arguments():
    '''

    issue: use color value instead of color name ?

    return Namespace object: {
        color: color name
        deliver: True or False
        separator: re.compile object
        conditions: (
            {func: color_by_field,
             fields: {1, -1, slice(2,None,2)},
             colors: (color names)},
            {func: color_by_pattern,
             pattern: re.compile object
             groups: {...},
             colors: (color names)},
            {}, ...
            )
    '''
    import argparse

    from .info import __version__
    from .attributes import attr_names

    parser = argparse.ArgumentParser(
        prog='ColorPrint',
        usage='...'*30,
        description='...(give example and how conditions work)',
        epilog='...'*30,
        )
    subparser = parser.add_subparsers(help='= =').add_parser('show')

    parser.add_argument(
        '-F', '--fields', metavar='condition',
        dest='conditions', nargs='+', action='append',
        type=type('F',(str,),{}),
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
        type=type('P',(str,),{}),
        help='...'*30,
        )
    parser.add_argument(
        '-C', '--color', metavar='color',
        nargs='+', #default=get_default_color(),
        help='...'*30,
        )
    parser.add_argument(
        '-D', '--deliver',
        action='store_true',
        help='...'*30,
        )
    parser.add_argument(
        '--version',
        action='version', version=__version__,
        )

    subparser.add_argument(
        '--16', metavar='attr',
        nargs='*',
        type=int,
        help='...'*30,
        )
    subparser.add_argument(
        '--256', metavar='attr',
        nargs='*',
        type=int,
        help='...'*30,
        )

    ns = parser.parse_args()
    return ns


def run_cmd():
    args = get_arguments()
    print(args)
