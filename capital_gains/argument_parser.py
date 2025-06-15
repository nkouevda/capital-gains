import argparse

from . import __version__


def get_parser():
    parser = argparse.ArgumentParser(
        prog="capital-gains",
        usage="%(prog)s [<options>] [--] <input file>",
        description="Capital gains calculator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "filename",
        type=str,
        help=argparse.SUPPRESS,
        metavar="<input file>",
    )

    parser.add_argument(
        "-d",
        "--decimal-places",
        dest="decimal_places",
        type=int,
        default=0,
        help="round $ to %(metavar)s decimal places",
        metavar="<n>",
    )
    parser.add_argument(
        "-s",
        "--shares-decimal-places",
        dest="shares_decimal_places",
        type=int,
        default=0,
        help="round shares to %(metavar)s decimal places",
        metavar="<n>",
    )
    parser.add_argument(
        "-t",
        "--totals",
        action="store_true",
        help="output totals",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose output",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    parser.add_argument(
        "-w",
        "--wash-sales",
        dest="wash_sales",
        action=argparse.BooleanOptionalAction,
        help="identify wash sales and adjust cost basis",
        default=True,
    )

    return parser
