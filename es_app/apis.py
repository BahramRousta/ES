import json

from rest_framework.response import Response
from rest_framework.views import APIView
from .aggrigstes import WalletAggregate
from es_app.models import Wallet
from .events import Deposit, Withdraw


class DepositView(APIView):

    def post(self, request):

        amount = request.data['amount']
        wallet = Wallet.objects.select_for_update().get(id=1)

        event = Deposit(amount=amount)
        aggr = WalletAggregate(wallet=wallet)
        aggr.events.append(event)
        aggr.apply_events()

        return Response(
            data={'Data': wallet.balance}
        )


class WithdrawView(APIView):

    def post(self, request):

        amount = request.data['amount']
        wallet = Wallet.objects.select_for_update().get(id=1)
        event = Withdraw(amount=amount)
        aggr = WalletAggregate(wallet=wallet)
        aggr.events.append(event)
        try:
            aggr.apply_events()

            return Response(
            data={'Data': wallet.balance}, status=200
            )
        except Exception as e:
            return Response(data={'Error': e.args}, status=400)