import decimal


def round_half_up(value, exponent):
  return value.quantize(exponent, rounding=decimal.ROUND_HALF_UP)


def format_dollars(value):
  return str(round_half_up(value, decimal.Decimal('1')))


def format_cents(value):
  return str(round_half_up(value, decimal.Decimal('1.00')))


def tabulate_closed_lots(closed_lots, format_decimal):
  header = [
      'description',
      'bought',
      'sold',
      'proceeds',
      'cost basis',
      'wash sale',
      'gain']

  return [header] + [[
      '%s %s (%s)' % (format_decimal(lot.shares), lot.symbol, lot.name),
      str(lot.buy.date),
      str(lot.sell.date),
      format_decimal(lot.proceeds),
      format_decimal(lot.cost_basis),
      format_decimal(lot.wash_sale),
      format_decimal(lot.gain)] for lot in closed_lots]


def tabulate_open_lots(open_lots, format_decimal):
  header = ['description', 'bought', 'cost basis']

  return [header] + [[
      '%s %s (%s)' % (format_decimal(lot.shares), lot.symbol, lot.name),
      str(lot.buy.date),
      format_decimal(lot.cost_basis)] for lot in open_lots]


def format_table(table):
  widths = [max(map(len, column)) for column in zip(*table)]

  return '\n'.join(
      ' | '.join(
          value.rjust(width)
          for value, width in zip(row, widths))
      for row in table)
