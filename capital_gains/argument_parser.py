import argparse

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
      '--cents',
      action='store_true',
      help='round to nearest cent, not dollar')
  parser.add_argument(
      '-v',
      '--version',
      action='version',
      version='%(prog)s ' + __version__)

  return parser
