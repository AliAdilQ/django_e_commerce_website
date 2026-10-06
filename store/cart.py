"""Session cart. Prices always come from the database, never from the browser."""
from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        raw = self.session.get("cart", {})
        self.data = {}
        if isinstance(raw, dict):
            for key, value in raw.items():
                try:
                    product_id, quantity = int(key), int(value)
                    if product_id > 0 and 1 <= quantity <= 999:
                        self.data[str(product_id)] = quantity
                except (TypeError, ValueError, OverflowError):
                    continue

    def save(self):
        self.session["cart"] = self.data
        self.session.modified = True

    def add(self, product, quantity=1, replace=False):
        quantity = quantity if replace else self.data.get(str(product.pk), 0) + quantity
        if not product.available or quantity > product.stock:
            raise ValueError(f"Only {product.stock if product.available else 0} of {product.name} are available.")
        if not 1 <= quantity <= 999:
            raise ValueError("Choose a quantity between 1 and 999.")
        self.data[str(product.pk)] = quantity
        self.save()

    def remove(self, product_id):
        self.data.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.data = {}
        self.save()

    def items(self):
        products = {str(p.pk): p for p in Product.objects.filter(pk__in=self.data).select_related("category")}
        missing = set(self.data) - set(products)
        for key in missing:
            self.data.pop(key)
        if missing:
            self.save()
        return [{"product": products[key], "quantity": qty, "price": products[key].current_price,
                 "subtotal": products[key].current_price * qty,
                 "stock_error": not products[key].available or qty > products[key].stock}
                for key, qty in self.data.items()]

    @property
    def count(self):
        return sum(item["quantity"] for item in self.items())

    @property
    def total(self):
        return sum((item["subtotal"] for item in self.items()), Decimal("0.00"))
