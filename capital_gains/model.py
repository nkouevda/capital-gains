import collections
import decimal


BaseTransaction = collections.namedtuple('Transaction', (
    'index',
    'date',
    'symbol',
    'name',
    'shares',
    'price',
    'fee'))


class Transaction(BaseTransaction):

  def split(self, shares):
    first = self._replace(
        shares=shares,
        fee=self.fee * shares / self.shares)

    second = self._replace(
        shares=self.shares - first.shares,
        fee=self.fee - first.fee)

    return first, second


class Lot(object):

  def __init__(self, buy):
    self.buy = buy

    self.adjustment = decimal.Decimal(0)
    self.sell = None
    self.wash_sale = decimal.Decimal(0)

  @property
  def index(self):
    return self.buy.index

  @property
  def symbol(self):
    return self.buy.symbol

  @property
  def name(self):
    return self.buy.name

  @property
  def shares(self):
    return self.buy.shares

  @property
  def cost_basis(self):
    return self.shares * self.buy.price + self.buy.fee + self.adjustment

  @property
  def proceeds(self):
    if self.sell is None:
      return None
    return self.shares * self.sell.price - self.sell.fee

  @property
  def gain(self):
    if self.proceeds is None:
      return None
    return self.proceeds - self.cost_basis + self.wash_sale

  def split(self, shares):
    first_buy, second_buy = self.buy.split(shares)

    first_lot = Lot(first_buy)
    first_lot.adjustment = self.adjustment * shares / self.shares

    second_lot = Lot(second_buy)
    second_lot.adjustment = self.adjustment - first_lot.adjustment

    return first_lot, second_lot
