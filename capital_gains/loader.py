import collections
import csv
import datetime
import decimal
import logging

from . import model


def load_transactions(filename):
  open_lots = collections.defaultdict(list)
  sells = collections.defaultdict(list)

  with open(filename, 'r') as in_file:
    reader = csv.reader(in_file)

    # Skip header
    next(reader)

    for index, (date, symbol, name, shares, price, fee) in enumerate(reader):
      date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
      name = name or None
      shares = decimal.Decimal(shares)
      price = decimal.Decimal(price)
      fee = decimal.Decimal(fee or 0)

      transaction = model.Transaction(index, date, symbol, name, abs(shares), price, fee)

      if shares > 0:
        lot = model.Lot(transaction)
        open_lots[symbol].append(lot)
        logging.debug(f'Added lot: {lot}')
      else:
        sells[symbol].append(transaction)
        logging.debug(f'Added sell: {transaction}')

  return open_lots, sells
