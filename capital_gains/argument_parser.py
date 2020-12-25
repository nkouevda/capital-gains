import argparse

import argparse_extensions

from . import __version__


def get_parser():
  parser = argparse.ArgumentParser(
      usage='%(prog)s [<options>] [--] <input file>',
      description='Capital gains calculator')

  parser.add_argument(
      'filename',
      type=str,
      help=argparse.SUPPRESS,
      metavar='<input file>')

  parser.add_argument(
      '-d',
      '--decimal-places',
      dest='decimal_places',
      type=int,
      default=0,
      help='round $ to %(metavar)s decimal places; default: %(default)s',
      metavar='<n>')
  parser.add_argument(
      '-s',
      '--shares-decimal-places',
      dest='shares_decimal_places',
      type=int,
      default=0,
      help='round shares to %(metavar)s decimal places; default: %(default)s',
      metavar='<n>')
  parser.add_argument(
      '-t',
      '--totals',
      action='store_true',
      help='output totals')
  parser.add_argument(
      '-v',
      '--verbose',
      action='store_true',
      help='verbose output')
  parser.add_argument(
      '-V',
      '--version',
      action='version',
      version='%(prog)s ' + __version__)
  parser.add_argument(
      '-w',
      '--wash-sales',
      dest='wash_sales',
      action=argparse_extensions.NegatableStoreTrueAction,
      help='identify wash sales and adjust cost basis; default: %(default)s',
      default=True)

  return parser
