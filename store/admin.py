from django.contrib import admin
from .models import Category, NewsletterSubscriber, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_price", "stock", "available", "featured", "created_at")
    list_filter = ("category", "available", "featured")
    list_editable = ("price", "stock", "available", "featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("category",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
