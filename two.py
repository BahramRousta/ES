from abc import ABC, abstractmethod
from dataclasses import dataclass


class Event(ABC):
    @abstractmethod
    def __repr__(self):
        pass


@dataclass(frozen=True)
class AddEvent(Event):
    title: str
    quantity: int
    price: float

    def __repr__(self):
        return f'Add Item {self.title} {self.quantity} {self.price} to cart'


@dataclass(frozen=True)
class RemoveEvent(Event):
    title: str

    def __repr__(self):
        return f'Remove Item {self.title} from cart'


@dataclass
class Product:
    id: int
    title: str
    quantity: int
    price: float


class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events


class Cart:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.products = []
        self.event_store = EventStore()

    def add_item(self, product: Product):
        event = AddEvent(title=product.title, quantity=product.quantity, price=product.price)
        self.event_store.append(event)
        self.products.append({
            'title': product.title,
            'quantity': product.quantity,
            'price': product.price
        })

    def remove_item(self, product: Product):
        event = RemoveEvent(title=product.title)
        self.event_store.append(event)
        self.products = [p for p in self.products if p['title'] != product.title]

    def get_cart_events(self):
        return self.event_store.get_events()



card = Cart(user_id=1)

product = Product(id=1, title='BMW', quantity=10, price=25000)
product_2 = Product(id=1, title='ZARA', quantity=100, price=325)

card.add_item(product)
card.add_item(product_2)
card.remove_item(product)

print(card.get_cart_events())
print(card.products)

