import datetime


class Event:
    """Base class for domain events"""
    def __init__(self, amount: float):
        self._amount = amount
        self._created_at = datetime.datetime.now()

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at


class CreateWallet(Event):
    def __repr__(self):
        return f'Created wallet at - {self.created_at}  with balance {self.amount}'


class DepositEvent(Event):
    def __repr__(self):
        return f'Deposit at - {self.created_at} from wallet with amount {self.amount}'


class WithdrawEvent(Event):
    def __repr__(self):
        return f'Withdraw at - {self.created_at} from wallet with amount {self.amount}'


class Wallet:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.balance = 0

        self.events = []

    def create(self, initial_balance: float = 0) -> 'Wallet':
        self.events.append(CreateWallet(initial_balance))
        self.balance = initial_balance
        return self

    def deposit(self, amount: float):
        if amount < 0:
            return ValueError('amount must be positive')

        self.balance += amount
        self.events.append(DepositEvent(amount))

    def withdraw(self, amount: float):
        if amount > self.balance:
            return ValueError('amount can not be greater than balance')
        self.balance -= amount
        self.events.append(WithdrawEvent(amount))

    def get_balance(self):
        return self.balance

    def get_balance_history(self):
        return [event.amount for event in self.events]

    def get_history(self) -> list:
        return self.events


wallet = Wallet(user_id=1).create()

print(wallet.get_balance())

wallet.deposit(1000)
wallet.deposit(5000)
wallet.withdraw(3250)
wallet.deposit(1563)
wallet.withdraw(4100)

print(wallet.get_balance())

print(wallet.get_history())
print(wallet.get_balance_history())

