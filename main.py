from enum import Enum


class OrderStatus(Enum):

    NEW = 'new'
    PAID = 'paid'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'


class Order:

    def __init__(self, user_id: int, status: str = 'new'):
        self.user_id = user_id
        self.status = status

    def set_status(self, new_status: str):
        if new_status not in OrderStatus():
            return ValueError('Invalid status - {}'.format(new_status))

        self.status = new_status
