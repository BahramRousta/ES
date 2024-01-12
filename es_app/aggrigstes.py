from es_app.events import Deposit, Withdraw
from django.db import transaction
import datetime
from es_app.models import Wallet, Event


class EventService:
    @classmethod
    def create_event(cls, wallet_id: int, event, status, balance):
        Event.objects.create(wallet_id=wallet_id,
                             type=event.__class__.__name__,
                             status=status,
                             balance=balance)


class WalletAggregate:

    def __init__(self, wallet: Wallet):
        self.wallet = wallet
        self.events = []
        self.event_service = EventService

    def add_event(self, event):
        self.events.append(event)

    def deposit(self, event):
        self.event_service.create_event(wallet_id=self.wallet.id,
                                        event=event,
                                        balance=self.wallet.balance,
                                        status=Event.Status.INITIAL)

        self.wallet.balance += event.amount
        self.wallet.created_at = datetime.datetime.now()
        self.wallet.save()
        self.event_service.create_event(wallet_id=self.wallet.id,
                                        event=event,
                                        balance=event.amount,
                                        status=Event.Status.FINALIZE)

    def withdraw(self, event):
        self.event_service.create_event(wallet_id=self.wallet.id,
                                        event=event,
                                        balance=self.wallet.balance,
                                        status=Event.Status.INITIAL)

        if self.wallet.balance < event.amount:
            self.event_service.create_event(wallet_id=self.wallet.id,
                                        event=event,
                                        balance=event.amount,
                                        status=Event.Status.FAILED)
            raise ValueError("Balance is out of range")
        else:
            self.wallet.balance -= event.amount
            self.wallet.created_at = datetime.datetime.now()
            self.wallet.save()
            self.event_service.create_event(wallet_id=self.wallet.id,
                                            event=event,
                                            balance=event.amount,
                                            status=Event.Status.FINALIZE)

    @transaction.atomic()
    def apply_events(self):
        try:
            for event in self.events:
                if isinstance(event, Deposit):
                    self.deposit(event)
                elif isinstance(event, Withdraw):
                    self.withdraw(event)
                else:
                    raise ValueError("Unknown transaction.")
        except Exception as e:
            raise ValueError(e.args)