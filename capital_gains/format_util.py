import decimal
import itertools


def round_half_up(value, exponent):
  return value.quantize(exponent, rounding=decimal.ROUND_HALF_UP)


def format_dollars(value):
  return str(round_half_up(value, decimal.Decimal('1')))


def format_cents(value):
  return str(round_half_up(value, decimal.Decimal('1.00')))


def tabulate_closed_lots(closed_lots, format_decimal):
  # Group parts of lots that were split (e.g. partially adjusted)
  # Only group if sold on the same day, and keep gains and losses separate
  grouped_lots = [list(group) for key, group in itertools.groupby(
      closed_lots, lambda lot: (
          lot.index, lot.sell.date, lot.proceeds > lot.cost_basis))]

  header = [
      'description',
      'acquired',
      'sold',
      'proceeds',
      'cost basis',
      'wash sale',
      'gain']

  return [header] + [
      [
          '%s %s (%s)' % (
              sum(lot.shares for lot in lots),
              lots[0].symbol,
              lots[0].name),
          str(lots[0].buy.date),
          str(lots[0].sell.date),
          format_decimal(sum(lot.proceeds for lot in lots)),
          format_decimal(sum(lot.cost_basis for lot in lots)),
          format_decimal(sum(lot.wash_sale for lot in lots)),
          format_decimal(sum(lot.gain for lot in lots))]
      for lots in grouped_lots]


def tabulate_open_lots(open_lots, format_decimal):
  # Group parts of lots that were split (e.g. partially adjusted)
  grouped_lots = [list(group) for index, group in itertools.groupby(
      open_lots, lambda lot: lot.index)]

  header = ['description', 'acquired', 'cost basis']

  return [header] + [
      [
          '%s %s (%s)' % (
              sum(lot.shares for lot in lots),
              lots[0].symbol,
              lots[0].name),
          str(lots[0].buy.date),
          format_decimal(sum(lot.cost_basis for lot in lots))]
      for lots in grouped_lots]


def format_table(table):
  widths = [max(map(len, column)) for column in zip(*table)]

  return '\n'.join(
      ' | '.join(
          value.rjust(width)
          for value, width in zip(row, widths))
      for row in table)
