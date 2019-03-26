from dataclasses import dataclass
from dataclasses import replace
import datetime
import decimal


@dataclass(frozen=True)
class Transaction(object):
  index: int
  date: datetime.datetime
  symbol: str
  name: str
  shares: decimal.Decimal
  price: decimal.Decimal
  fee: decimal.Decimal

  def split(self, shares):
    first = replace(
        self,
        shares=shares,
        fee=self.fee * shares / self.shares)

    second = replace(
        self,
        shares=self.shares - first.shares,
        fee=self.fee - first.fee)

    return first, second


# Mutable! `adjustment`, `sell`, and `wash_sale` are assigned in main logic
@dataclass
class Lot(object):
  buy: Transaction
  adjustment: decimal.Decimal = decimal.Decimal(0)
  sell: Transaction = None
  wash_sale: decimal.Decimal = decimal.Decimal(0)

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

    first_lot = Lot(
        buy=first_buy,
        adjustment=self.adjustment * shares / self.shares)

    second_lot = Lot(
        buy=second_buy,
        adjustment=self.adjustment - first_lot.adjustment)

    return first_lot, second_lot
