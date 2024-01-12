from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):

    owner = models.ForeignKey(User, related_name='wallet', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Event(models.Model):

    class Type(models.TextChoices):

        DEPOSIT = "deposit"
        WITHDRAW = "withdraw"

    class Status(models.TextChoices):
        INITIAL = "initial"
        PENDING = "pending"
        FINALIZE = "finalize"
        FAILED = "fail"

    wallet = models.ForeignKey(Wallet, related_name='events', on_delete=models.PROTECT)
    type = models.TextField(choices=Type)
    status = models.TextField(choices=Status)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
