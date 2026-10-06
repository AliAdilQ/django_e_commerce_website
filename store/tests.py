from decimal import Decimal
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from .models import Category, NewsletterSubscriber, Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics", slug="electronics")
        cls.product = Product.objects.create(name="Wireless Headphones", slug="wireless-headphones",
            category=cls.category, description="Soft headphones with balanced audio", short_description="Daily sound",
            price="89.00", discount_price="69.00", stock=10, featured=True)

    def test_homepage_and_navigation(self):
        response = self.client.get("/")
        self.assertContains(response, "Good finds.")
        self.assertContains(response, self.product.name)
        self.assertContains(response, "bootstrap.min.css")

    def test_shop_and_category(self):
        self.assertContains(self.client.get(reverse("store:shop")), self.product.name)
        self.assertContains(self.client.get(self.category.get_absolute_url()), self.product.name)
        self.assertEqual(self.client.get("/category/missing/").status_code, 404)

    def test_product_details_and_unavailable_product(self):
        self.assertContains(self.client.get(self.product.get_absolute_url()), "$69.00")
        self.product.available = False
        self.product.save()
        self.assertEqual(self.client.get(self.product.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse("store:shop")), self.product.name)

    def test_search_name_description_and_category(self):
        for query in ("Wireless", "balanced", "Electronics"):
            response = self.client.get(reverse("store:search"), {"q": query})
            self.assertEqual(response.context["page_obj"].paginator.count, 1)
        self.assertContains(self.client.get("/search/", {"q": "nothing-matches"}), "No finds just yet.")

    def test_price_sort_uses_discounted_price(self):
        other = Product.objects.create(name="Speaker", slug="speaker", category=self.category,
            price="75.00", stock=5, short_description="Sound", description="Speaker")
        ascending = self.client.get("/shop/", {"sort": "price_asc"}).context["page_obj"]
        self.assertEqual(list(ascending), [self.product, other])
        descending = self.client.get("/shop/", {"sort": "price_desc"}).context["page_obj"]
        self.assertEqual(list(descending), [other, self.product])

    def test_sale_and_stock_filters(self):
        self.assertEqual(self.client.get("/shop/?sale=1").context["page_obj"].paginator.count, 1)
        self.product.stock = 0
        self.product.save()
        self.assertEqual(self.client.get("/shop/?stock=1").context["page_obj"].paginator.count, 0)

    def test_pagination_and_invalid_sort(self):
        for i in range(14):
            Product.objects.create(name=f"Product {i}", slug=f"product-{i}", category=self.category,
                price="10.00", stock=2, description="A useful item", short_description="Demo")
        page_one = self.client.get("/shop/", {"sort": "not-a-field"})
        self.assertEqual(len(page_one.context["page_obj"]), 12)
        self.assertEqual(page_one.context["sort"], "newest")
        self.assertEqual(len(self.client.get("/shop/?page=2").context["page_obj"]), 3)
        self.assertEqual(self.client.get("/shop/?page=invalid").status_code, 200)

    def test_product_properties_and_discount_constraint(self):
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_price, Decimal("69.00"))
        self.assertEqual(self.product.discount_percentage, 22)
        self.assertTrue(self.product.in_stock)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.filter(pk=self.product.pk).update(discount_price=Decimal("90.00"))

    def test_newsletter_is_validated_and_idempotent(self):
        self.client.post("/newsletter/", {"email": "alex@example.com"})
        self.client.post("/newsletter/", {"email": "ALEX@example.com"})
        self.client.post("/newsletter/", {"email": "invalid"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        self.assertEqual(self.client.get("/newsletter/").status_code, 405)

    @override_settings(DEBUG=False)
    def test_styled_404_and_500_templates(self):
        from django.views.defaults import server_error
        from django.test import RequestFactory
        self.assertContains(self.client.get("/not-a-real-page/"), "This find has wandered off.", status_code=404)
        response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"A little pause", response.content)

    def test_about_and_support_pages(self):
        self.assertContains(self.client.get("/about/"), "A collection with intention.")
        self.assertContains(self.client.get("/support/"), "Payments & privacy")


class CartTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Home", slug="home")
        cls.product = Product.objects.create(name="Mug", slug="mug", category=category,
            price="18.00", discount_price="15.00", stock=5, description="Ceramic", short_description="Warm mornings")

    def add(self, quantity=1, **extra):
        return self.client.post(reverse("store:cart_add", args=[self.product.pk]), {"quantity": quantity, **extra})

    def test_guest_can_add_update_and_remove(self):
        self.add(2)
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 2)
        response = self.client.get("/cart/")
        self.assertEqual(response.context["total"], Decimal("30.00"))
        self.assertEqual(response.context["cart_count"], 2)
        self.client.post(reverse("store:cart_update", args=[self.product.pk]), {"quantity": 3})
        self.assertEqual(self.client.get("/cart/").context["total"], Decimal("45.00"))
        self.client.post(reverse("store:cart_remove", args=[self.product.pk]))
        self.assertEqual(self.client.session["cart"], {})

    def test_quantity_validation_and_combined_stock(self):
        for quantity in (-1, 0, "oops", 1000, 6):
            self.add(quantity)
            self.assertEqual(self.client.get("/cart/").context["cart_count"], 0)
        self.add(4)
        self.add(2)
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 4)

    def test_cart_mutations_require_post(self):
        for name in ("cart_add", "cart_update", "cart_remove"):
            self.assertEqual(self.client.get(reverse(f"store:{name}", args=[self.product.pk])).status_code, 405)

    def test_open_redirect_is_rejected(self):
        self.assertRedirects(self.add(next="https://evil.example/"), "/cart/")
        self.assertRedirects(self.add(next="/shop/"), "/shop/")

    def test_csrf_is_enforced(self):
        secure_client = Client(enforce_csrf_checks=True)
        response = secure_client.post(reverse("store:cart_add", args=[self.product.pk]), {"quantity": 1})
        self.assertEqual(response.status_code, 403)

    def test_stock_changes_are_visible(self):
        self.add(3)
        self.product.stock = 1
        self.product.save()
        response = self.client.get("/cart/")
        self.assertTrue(response.context["has_stock_error"])
        self.assertContains(response, "Stock changed")

    def test_deleted_product_is_removed_from_cart(self):
        self.add()
        self.product.delete()
        self.assertEqual(self.client.get("/cart/").context["cart_count"], 0)
        self.assertEqual(self.client.session["cart"], {})

    def test_malformed_session_cart_is_ignored(self):
        session = self.client.session
        session["cart"] = {"oops": "wrong", str(self.product.pk): -1}
        session.save()
        self.assertEqual(self.client.get("/cart/").context["cart_count"], 0)


class SeedTests(TestCase):
    def test_seed_is_repeatable_and_preserves_edits(self):
        with TemporaryDirectory(dir=Path.cwd()) as directory, override_settings(DEBUG=True, MEDIA_ROOT=Path(directory)/"media", BASE_DIR=Path(directory)):
            call_command("seed_demo", stdout=StringIO())
            product = Product.objects.get(slug="wireless-headphones")
            self.assertTrue(Path(product.image.path).exists())
            product.stock = 7
            product.price = Decimal("99.00")
            product.save()
            admin = get_user_model().objects.get(username="admin")
            self.assertTrue(admin.check_password("Admin12345!"))
            admin.set_password("ChangedPassword987!")
            admin.save()
            call_command("seed_demo", stdout=StringIO())
            self.assertEqual(Category.objects.count(), 6)
            self.assertEqual(Product.objects.count(), 22)
            self.assertEqual(get_user_model().objects.count(), 2)
            product.refresh_from_db()
            admin.refresh_from_db()
            self.assertEqual(product.stock, 7)
            self.assertEqual(product.price, Decimal("99.00"))
            self.assertTrue(admin.check_password("ChangedPassword987!"))

    @override_settings(DEBUG=False)
    def test_seed_refuses_production_settings(self):
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command("seed_demo", stdout=StringIO())
