import logging


def process_sells(open_lots, sells, wash_sales):
  closed_lots = []

  # One sell at a time: first identify all closing lots, then handle wash sales
  while sells:
    sell = sells.pop(0)
    remaining_shares = abs(sell.shares)
    logging.debug(f'Processing sell: {sell}')

    closable_lots = [
        lot for lot in open_lots
        if lot.index < sell.index
        and (sell.name is None or lot.name == sell.name)]
    closing_lots = []

    while remaining_shares:
      closing_lot = closable_lots.pop(0)
      logging.debug(f'Closing lot: {closing_lot}')

      # Split sell if lot is too small, or vice versa
      if closing_lot.shares < remaining_shares:
        logging.debug(f'Splitting sell: {sell}')
        sell, remaining_sell = sell.split(closing_lot.shares)
        sells.insert(0, remaining_sell)
        remaining_shares = abs(sell.shares)
        logging.debug(f'Split sell into: {sell} + {remaining_sell}')
      elif closing_lot.shares > remaining_shares:
        logging.debug(f'Splitting closing lot: {closing_lot}')
        open_index = open_lots.index(closing_lot)
        closing_lot, remaining_lot = closing_lot.split(remaining_shares)
        open_lots[open_index:open_index + 1] = [closing_lot, remaining_lot]
        closable_lots.insert(0, remaining_lot)
        logging.debug(f'Split closing lot into: {closing_lot} + {remaining_lot}')

      closing_lot.sell = sell
      open_lots.remove(closing_lot)
      closing_lots.append(closing_lot)
      remaining_shares -= closing_lot.shares

    for closing_lot in closing_lots:
      # Gains can be closed immediately, but check losses for wash sales
      if closing_lot.gain < 0:
        remaining_shares = closing_lot.shares
        remaining_loss = abs(closing_lot.gain)

        adjustable_lots = [
            lot for lot in open_lots
            if (abs((lot.buy.date - closing_lot.sell.date).days) <= 30
                and lot.index != closing_lot.index
                and lot.name != closing_lot.name
                and lot.adjustment == 0)]

        if not adjustable_lots:
          logging.debug(f'Loss of {remaining_loss}; no wash sale')
        else:
          if not wash_sales:
            logging.debug(
                f'Loss of {remaining_loss}; wash sale; not adjusting lots because --no-wash-sales')
          else:
            logging.debug(f'Loss of {remaining_loss}; wash sale; adjusting lots')

            while remaining_shares and adjustable_lots:
              logging.debug(f'Remaining shares to adjust: {remaining_shares}')
              adjusting_lot = adjustable_lots.pop(0)

              # Split adjustable lot if too large
              if adjusting_lot.shares > remaining_shares:
                logging.debug(f'Splitting adjustable lot: {adjusting_lot}')
                open_index = open_lots.index(adjusting_lot)
                adjusting_lot, remaining_lot = adjusting_lot.split(remaining_shares)
                open_lots[open_index:open_index + 1] = [adjusting_lot, remaining_lot]
                adjustable_lots.insert(0, remaining_lot)
                logging.debug(f'Split adjustable lot into: {adjusting_lot} + {remaining_lot}')

              adjusting_lot.adjustment = remaining_loss * adjusting_lot.shares / remaining_shares
              logging.debug(f'Adjusted lot: {adjusting_lot}')

              remaining_shares -= adjusting_lot.shares
              remaining_loss -= adjusting_lot.adjustment

          if remaining_shares:
            logging.debug(f'Finished adjusting; remaining loss of {remaining_loss} is realized')

        closing_lot.wash_sale = abs(closing_lot.gain) * (
            closing_lot.shares - remaining_shares) / closing_lot.shares

      closed_lots.append(closing_lot)
      logging.debug(f'Closed lot: {closing_lot}')

  return closed_lots
