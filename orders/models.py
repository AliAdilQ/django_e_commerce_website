import uuid
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class Payment(models.TextChoices):
        COD = "cod", "Cash on Delivery"
        DEMO_CARD = "demo_card", "Demo Card Payment"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    checkout_token = models.UUIDField(unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    payment_method = models.CharField(max_length=20, choices=Payment.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.number

    @property
    def number(self):
        return f"NS-{self.pk:05d}" if self.pk else "New order"

    def get_absolute_url(self):
        return reverse("orders:detail", args=[self.reference])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("store.Product", on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=150)
    product_image = models.CharField(max_length=250, blank=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(quantity__gt=0), name="positive_order_quantity")]

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"

    @property
    def subtotal(self):
        return self.price * self.quantity
