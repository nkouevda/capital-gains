import collections
import csv
import datetime
import decimal
import itertools

from . import argument_parser
from . import format_util
from . import model


def read_transactions(filename):
  open_lots = collections.defaultdict(list)
  sells = collections.defaultdict(list)

  with open(filename) as in_file:
    reader = csv.reader(in_file)

    # Skip header
    next(reader)

    for index, (date, symbol, name, shares, price, fee) in enumerate(reader):
      date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
      name = name or None
      shares = decimal.Decimal(shares)
      price = decimal.Decimal(price)
      fee = decimal.Decimal(fee or 0)

      transaction = model.Transaction(
          index, date, symbol, name, abs(shares), price, fee)

      if shares > 0:
        lot = model.Lot(transaction)
        open_lots[symbol].append(lot)
      else:
        sells[symbol].append(transaction)

  return open_lots, sells


def process_sells(open_lots, sells):
  closed_lots = []

  # One sell at a time: first identify all closing lots, then handle wash sales
  while sells:
    sell = sells.pop(0)
    remaining_shares = abs(sell.shares)

    closable_lots = [
        lot for lot in open_lots
        if lot.index < sell.index
        and (sell.name is None or lot.name == sell.name)]
    closing_lots = []

    while remaining_shares:
      closing_lot = closable_lots.pop(0)

      # Split sell if lot is too small, or vice versa
      if closing_lot.shares < remaining_shares:
        sell, remaining_sell = sell.split(closing_lot.shares)
        sells.insert(0, remaining_sell)
        remaining_shares = abs(sell.shares)
      elif closing_lot.shares > remaining_shares:
        open_index = open_lots.index(closing_lot)
        closing_lot, remaining_lot = closing_lot.split(remaining_shares)
        open_lots[open_index:open_index + 1] = [closing_lot, remaining_lot]
        closable_lots.insert(0, remaining_lot)

      closing_lot.sell = sell
      open_lots.remove(closing_lot)
      closing_lots.append(closing_lot)
      remaining_shares -= closing_lot.shares

    for closing_lot in closing_lots:
      if closing_lot.gain < 0:
        remaining_shares = closing_lot.shares
        remaining_loss = abs(closing_lot.gain)

        adjustable_lots = [
            lot for lot in open_lots
            if (abs((lot.buy.date - closing_lot.sell.date).days) <= 30
                and lot.index != closing_lot.index
                and lot.name != closing_lot.name
                and lot.adjustment == 0)]

        while remaining_shares and adjustable_lots:
          adjusting_lot = adjustable_lots.pop(0)

          # Split lot if too large
          if adjusting_lot.shares > remaining_shares:
            open_index = open_lots.index(adjusting_lot)
            adjusting_lot, remaining_lot = adjusting_lot.split(remaining_shares)
            open_lots[open_index:open_index + 1] = [
                adjusting_lot, remaining_lot]
            adjustable_lots.insert(0, remaining_lot)

          adjusting_lot.adjustment = (
              remaining_loss * adjusting_lot.shares / remaining_shares)
          remaining_shares -= adjusting_lot.shares
          remaining_loss -= adjusting_lot.adjustment

        closing_lot.wash_sale = abs(closing_lot.gain) * (
            closing_lot.shares - remaining_shares) / closing_lot.shares

      closed_lots.append(closing_lot)

  return closed_lots


def main():
  parser = argument_parser.get_parser()
  args = parser.parse_args()

  format_decimal = (
      format_util.format_cents if args.cents else format_util.format_dollars)

  open_lots, sells = read_transactions(args.filename)
  closed_lots = collections.defaultdict(list)

  for symbol, symbol_sells in sells.items():
    closed_lots[symbol] = process_sells(open_lots[symbol], symbol_sells)

  if closed_lots:
    print('Closed lots:')
    print()
    flattened_lots = itertools.chain.from_iterable(closed_lots.values())
    table = format_util.tabulate_closed_lots(flattened_lots, format_decimal)
    print(format_util.format_table(table))

  if any(open_lots.values()):
    if closed_lots:
      print()

    print('Open lots:')
    print()
    flattened_lots = itertools.chain.from_iterable(open_lots.values())
    table = format_util.tabulate_open_lots(flattened_lots, format_decimal)
    print(format_util.format_table(table))


if __name__ == '__main__':
  main()
