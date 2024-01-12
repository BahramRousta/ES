import datetime
from dataclasses import dataclass


class Event:
    created: datetime = datetime.datetime.now()


@dataclass(frozen=True)
class WalletCreated(Event):
    user_id: int


@dataclass(frozen=True)
class Deposit(Event):
    amount: float


@dataclass(frozen=True)
class Withdraw(Event):
    amount: float