from .parse_args import create_parser
from .show_colors import (
    format_color as to_code,
    COLOR16,
    COLOR256,
    )
from .coloring import colorprint


def run_cmd():
    parser = create_parser()
    args = parser.parse_args()
    attributes = args.show16 or args.show256

    if   args.show16=='':
        parser.exit(status=0, message=COLOR16)
    elif args.show256=='':
        parser.exit(status=0, message=COLOR256)
    elif attributes:
        parser.exit(status=0, message=to_code(attributes))
    elif args.conditions is not None:
        try:
            colorprint(args)
        except Exception as E:
            parser.error(message=E.args[0])
    else:
        parser.exit(status=1, message=parser.format_help())
