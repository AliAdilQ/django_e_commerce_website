"""Atomic, stock-checked order creation with immutable item price snapshots."""
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from store.models import Product
from .models import Order, OrderItem


class CheckoutError(ValueError):
    pass


@transaction.atomic
def place_order(user, cart_data, checkout_data):
    data = dict(checkout_data)
    token = data.pop("checkout_token")
    existing = Order.objects.filter(checkout_token=token, user=user).first()
    if existing:
        return existing
    if not cart_data:
        raise CheckoutError("Your bag is empty. Add something you love first.")
    products = {str(p.pk): p for p in Product.objects.select_for_update().filter(pk__in=cart_data)}
    snapshots = []
    total = Decimal("0.00")
    for key, quantity in cart_data.items():
        product = products.get(str(key))
        if not product or not product.available:
            raise CheckoutError("An item is no longer available. Please review your bag.")
        if not isinstance(quantity, int) or not 1 <= quantity <= min(product.stock, 999):
            raise CheckoutError(f"There isn't enough stock for {product.name}. Please review your bag.")
        updated = Product.objects.filter(pk=product.pk, available=True, stock__gte=quantity).update(stock=F("stock") - quantity)
        if updated != 1:
            raise CheckoutError(f"{product.name} just sold out. Please review your bag.")
        snapshots.append((product, quantity))
        total += product.current_price * quantity
    order = Order.objects.create(user=user, checkout_token=token, total_amount=total, **data)
    OrderItem.objects.bulk_create([
        OrderItem(order=order, product=product, product_name=product.name,
                  product_image=product.image.name, quantity=quantity, price=product.current_price)
        for product, quantity in snapshots
    ])
    return order
