from enum import Enum
from events import OrderCreated, StatusChanged


class OrderStatus(Enum):

    NEW = 'new'
    PAID = 'paid'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'


class Order:

    def __init__(self, user_id: int, status: str = 'new'):
        self.user_id = user_id
        self.status = status
        self.events = ['new']
        self.changed = []

    def set_status(self, new_status: str):
        if new_status.upper() not in OrderStatus.__members__:
            return ValueError('Invalid status - {}'.format(new_status))

        self.status = new_status
        self.events.append(new_status)

        event = StatusChanged(new_status)
        self.changed.append(event)

    def get_status(self):
        return self.status

    def get_events(self):
        return [str(change) for change in self.changed]


order = Order(user_id=1) # 1
order.set_status('confirmed')  # 2
order.set_status('paid')  # 3
order.set_status('shipped')  # 4

print(order.get_status())
print(order.get_events())