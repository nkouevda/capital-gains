import datetime
import decimal
from dataclasses import dataclass
from dataclasses import replace


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
            fee=self.fee * shares / self.shares,
        )

        second = replace(
            self,
            shares=self.shares - first.shares,
            fee=self.fee - first.fee,
        )

        return first, second


# Mutable! `adjustment`, `sale`, and `wash_sale` are assigned in main logic
@dataclass
class Lot(object):
    purchase: Transaction
    adjustment: decimal.Decimal = decimal.Decimal(0)
    sale: Transaction = None
    wash_sale: decimal.Decimal = decimal.Decimal(0)

    @property
    def index(self):
        return self.purchase.index

    @property
    def symbol(self):
        return self.purchase.symbol

    @property
    def name(self):
        return self.purchase.name

    @property
    def shares(self):
        return self.purchase.shares

    @property
    def cost_basis(self):
        return self.shares * self.purchase.price + self.purchase.fee + self.adjustment

    @property
    def proceeds(self):
        if self.sale is None:
            return None
        return self.shares * self.sale.price - self.sale.fee

    @property
    def gain(self):
        if self.proceeds is None:
            return None
        return self.proceeds - self.cost_basis + self.wash_sale

    def split(self, shares):
        first_purchase, second_purchase = self.purchase.split(shares)

        first_lot = Lot(
            purchase=first_purchase,
            adjustment=self.adjustment * shares / self.shares,
        )

        second_lot = Lot(
            purchase=second_purchase,
            adjustment=self.adjustment - first_lot.adjustment,
        )

        return first_lot, second_lot
