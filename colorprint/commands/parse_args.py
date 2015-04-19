usage = '''
       ColorPrint [-h] [--version]
                  [--show16 [attr [attr ...]] | --show256[attr [attr ...]]]
                  [-D color [color ...]]
                  [-F condition [condition ...]] [-S sep]
                  [-P condition [condition ...]]
    '''

def create_parser():
    import argparse

    from ..attributes import default_color
    from ..info import __version__

    parser = argparse.ArgumentParser(
        prog='ColorPrint',
        description='...(give example and how conditions work)',
        epilog='...'*30,
        usage=usage.strip(),
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
