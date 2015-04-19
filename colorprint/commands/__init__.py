from .parse_args import create_parser
from .show_colors import gen_color_info
from .coloring import colorprint


def run_cmd():
    parser = create_parser()
    args = parser.parse_args()

    if not (args.show16 is args.show256 is None):
        color_info = gen_color_info(args.show16, args.show256)
        parser.exit(status=0, message=color_info)
    elif args.conditions is not None:
        try:
            colorprint(args)
        except Exception as E:
            parser.error(message=E.args[0])
    else:
        parser.exit(status=1, message=parser.format_help())
