from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    icon = models.CharField(max_length=30, default="grid")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField()
    short_description = models.CharField(max_length=240)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         validators=[MinValueValidator(Decimal("0.01"))])
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True)
    featured = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(condition=Q(price__gt=0), name="positive_product_price"),
            models.CheckConstraint(condition=Q(discount_price__isnull=True) | (
                Q(discount_price__gt=0) & Q(discount_price__lt=F("price"))), name="valid_product_discount"),
        ]
        indexes = [models.Index(fields=["available", "featured"])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product", args=[self.slug])

    @property
    def current_price(self):
        return self.discount_price if self.discount_price is not None else self.price

    @property
    def discount_percentage(self):
        return round((1 - self.current_price / self.price) * 100) if self.discount_price else 0

    @property
    def in_stock(self):
        return self.available and self.stock > 0

    @property
    def is_new(self):
        return self.created_at >= timezone.now() - timedelta(days=30)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
