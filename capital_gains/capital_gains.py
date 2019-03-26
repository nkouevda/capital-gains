import collections

from . import argument_parser
from . import formatter
from . import loader
from . import logic


def main():
  parser = argument_parser.get_parser()
  args = parser.parse_args()

  open_lots, sells = loader.load_transactions(args.filename)
  closed_lots = collections.defaultdict(list)

  for symbol, symbol_sells in sells.items():
    closed_lots[symbol] = logic.process_sells(open_lots[symbol], symbol_sells)

  output = formatter.format(
      closed_lots,
      open_lots,
      args.decimal_places,
      args.shares_decimal_places,
      args.totals)
  print(output)


if __name__ == '__main__':
  main()
