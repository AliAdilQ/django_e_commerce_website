from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from store.demo_art import hero_art, product_art
from store.demo_data import CATEGORIES, DETAILS, PRODUCTS
from store.models import Category, Product


class Command(BaseCommand):
    help = "Create the local NovaShop catalog, original images, and demo accounts without overwriting existing data."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Demo accounts are development-only. seed_demo requires DJANGO_DEBUG=True.")
        User = get_user_model()
        for username, password, email, staff in [
            ("admin", "Admin12345!", "admin@example.com", True),
            ("demo_user", "Demo12345!", "demo@example.com", False),
        ]:
            user, created = User.objects.get_or_create(username=username, defaults={
                "email": email, "is_staff": staff, "is_superuser": staff,
                "first_name": "Nova" if staff else "Alex", "last_name": "Admin" if staff else "Morgan",
            })
            if created:
                user.set_password(password)
                user.save()
            self.stdout.write(f"{'Created' if created else 'Kept existing'} account: {username}")
        categories = {}
        for name, slug, icon, description in CATEGORIES:
            categories[slug], _ = Category.objects.get_or_create(slug=slug, defaults={
                "name": name, "icon": icon, "description": description,
            })
        added = 0
        for name, category, price, sale, stock, featured, art, summary in PRODUCTS:
            slug = "wireless-headphones" if art == "headphones" else slugify(name)
            relative_path = f"products/demo/{slug}.png"
            path = settings.MEDIA_ROOT / relative_path
            if not path.exists():
                product_art(art, path)
            product, created = Product.objects.get_or_create(slug=slug, defaults={
                "name": name, "category": categories[category], "description": DETAILS[art],
                "short_description": summary, "price": Decimal(price),
                "discount_price": Decimal(sale) if sale else None, "stock": stock,
                "featured": featured, "image": relative_path,
            })
            if not product.image:
                product.image = relative_path
                product.save(update_fields=["image"])
            added += int(created)
        hero_path = settings.BASE_DIR / "static" / "images" / "hero-headphones.png"
        if not hero_path.exists():
            hero_art(hero_path)
        self.stdout.write(self.style.SUCCESS(
            f"NovaShop ready: {len(CATEGORIES)} categories, {len(PRODUCTS)} demo products ({added} new). "
            "Existing prices, stock, accounts, and orders were preserved."
        ))
