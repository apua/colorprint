from .info import __version__


def get_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        prog='ColorPrint',
        usage='...'*30,
        description='...(give example and how conditions work)',
        epilog='...'*30,
        )
    parser.add_argument(
        '-F', '--fields', metavar='condition',
        dest='conditions', nargs='+', action='append',
        #assertion=None,
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
        help='...'*30,
        )
    parser.add_argument(
        '-C', '--color', metavar='color',
        nargs='+',
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
    return parser.parse_args()


def run_cmd():
    args = get_arguments()
    print(args)
