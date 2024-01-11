

class Wallet:

    def __init__(self, user_id: int, balance: float):
        self.user_id = user_id
        self.balance = balance

        self.events = ['new']

    def create(self):
        ...

    def deposit(self, amount: float):
        if amount < 0:
            return ValueError('amount must be positive')

        self.balance += amount
        self.events.append('deposit')

    def withdraw(self, amount: float):
        if amount > self.balance:
            return ValueError('amount can not be greater than balance')
        self.balance -= amount
        self.events.append('withdraw')

    def get_balance(self):
        return self.balance

    def get_history(self) -> list:
        return self.events


wallet = Wallet(user_id=1, balance=0)

print(wallet.get_balance())

wallet.deposit(1000)
wallet.deposit(5000)
wallet.withdraw(3250)
wallet.deposit(1563)
wallet.withdraw(4100)

print(wallet.get_balance())

print(wallet.get_history())

