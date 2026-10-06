import uuid
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product
from .models import Order
from .services import CheckoutError, place_order


class CheckoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("customer", "alex@example.com", "Password888!")
        cls.other_user = get_user_model().objects.create_user("other", "other@example.com", "Password888!")
        category = Category.objects.create(name="Home", slug="home")
        cls.product = Product.objects.create(name="Ceramic Mug", slug="ceramic-mug", category=category,
            price="18.00", discount_price="15.00", stock=5, short_description="Warm", description="Warm mornings")
        cls.other = Product.objects.create(name="Lamp", slug="lamp", category=category,
            price="45.00", stock=2, short_description="Light", description="Bright ideas")

    def shipping(self, token=None):
        return {"full_name": "Alex Morgan", "email": "alex@example.com", "phone": "+62 81234567890",
                "address": "12 Example Lane", "city": "Jakarta", "postal_code": "10110", "country": "Indonesia",
                "payment_method": "demo_card", "checkout_token": token or uuid.uuid4()}

    def prepare(self):
        self.client.force_login(self.user)
        self.client.post(reverse("store:cart_add", args=[self.product.pk]), {"quantity": 2})
        self.client.get("/orders/checkout/")
        return self.shipping(self.client.session["checkout_token"])

    def test_checkout_creates_order_updates_stock_and_clears_cart(self):
        data = self.prepare()
        data["total_amount"] = "0.01"
        data["price"] = "0.01"
        response = self.client.post("/orders/checkout/", data)
        order = Order.objects.get()
        self.assertRedirects(response, reverse("orders:confirmation", args=[order.reference]))
        self.assertEqual(order.total_amount, Decimal("30.00"))
        self.assertEqual(order.items.get().price, Decimal("15.00"))
        self.assertEqual(order.items.get().quantity, 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(self.client.session["cart"], {})

    def test_duplicate_submission_does_not_duplicate_order(self):
        data = self.prepare()
        first = self.client.post("/orders/checkout/", data)
        second = self.client.post("/orders/checkout/", data)
        self.assertEqual(first.url, second.url)
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_atomic_rollback_when_another_item_is_out_of_stock(self):
        with self.assertRaises(CheckoutError):
            place_order(self.user, {str(self.product.pk): 2, str(self.other.pk): 3}, self.shipping())
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
        self.assertEqual(Order.objects.count(), 0)

    def test_changed_stock_blocks_checkout_and_keeps_cart(self):
        data = self.prepare()
        Product.objects.filter(pk=self.product.pk).update(stock=1)
        response = self.client.post("/orders/checkout/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 2)

    def test_unavailable_product_and_empty_cart_rejected(self):
        self.product.available = False
        self.product.save()
        for cart in ({str(self.product.pk): 1}, {}):
            with self.assertRaises(CheckoutError):
                place_order(self.user, cart, self.shipping())

    def test_checkout_token_and_delivery_validation(self):
        data = self.prepare()
        data["checkout_token"] = str(uuid.uuid4())
        response = self.client.post("/orders/checkout/", data)
        self.assertTrue(response.context["form"].non_field_errors())
        data["phone"] = "123"
        data["email"] = "invalid"
        response = self.client.post("/orders/checkout/", data)
        self.assertIn("phone", response.context["form"].errors)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(Order.objects.count(), 0)

    def test_anonymous_checkout_and_history_require_login(self):
        for path in ("/orders/checkout/", "/orders/"):
            self.assertEqual(self.client.get(path).status_code, 302)
            self.assertIn("/accounts/login/?next=", self.client.get(path).url)

    def test_orders_are_private_to_the_owner(self):
        order = place_order(self.user, {str(self.product.pk): 1}, self.shipping())
        self.client.force_login(self.other_user)
        self.assertNotContains(self.client.get("/orders/"), order.number)
        self.assertEqual(self.client.get(order.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(reverse("orders:confirmation", args=[order.reference])).status_code, 404)
        self.client.force_login(self.user)
        self.assertContains(self.client.get("/orders/"), order.number)
        self.assertEqual(self.client.get(order.get_absolute_url()).status_code, 200)

    def test_order_snapshots_survive_product_changes_and_deletion(self):
        order = place_order(self.user, {str(self.product.pk): 2}, self.shipping())
        self.product.name = "Changed name"
        self.product.discount_price = None
        self.product.price = Decimal("99.00")
        self.product.save()
        item = order.items.get()
        self.assertEqual(item.product_name, "Ceramic Mug")
        self.assertEqual(item.price, Decimal("15.00"))
        self.product.delete()
        item.refresh_from_db()
        self.assertIsNone(item.product)
        self.assertEqual(item.subtotal, Decimal("30.00"))

    def test_empty_checkout_redirects_to_shop(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get("/orders/checkout/"), "/shop/")

    def test_guest_cart_survives_login(self):
        self.client.post(reverse("store:cart_add", args=[self.product.pk]), {"quantity": 1})
        self.client.post("/accounts/login/", {"username": "customer", "password": "Password888!"})
        self.assertEqual(self.client.get("/cart/").context["cart_count"], 1)

    def test_admin_requires_staff_and_lists_models(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/admin/").status_code, 302)
        admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "AdminPassword888!")
        self.client.force_login(admin)
        response = self.client.get("/admin/")
        self.assertContains(response, "NovaShop administration")
        self.assertContains(response, "Products")
        self.assertContains(response, "Orders")
