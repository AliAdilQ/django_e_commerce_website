from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity", "subtotal")
    can_delete = False
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "full_name", "user", "total_amount", "status", "payment_method", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("full_name", "email", "user__username")
    list_editable = ("status",)
    list_select_related = ("user",)
    inlines = (OrderItemInline,)
    readonly_fields = ("reference", "checkout_token", "user", "full_name", "email", "phone", "address", "city",
                       "postal_code", "country", "total_amount", "payment_method", "created_at")
    def has_add_permission(self, request):
        return False

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "quantity", "price", "subtotal")
    search_fields = ("product_name", "order__full_name")
    readonly_fields = ("order", "product", "product_name", "product_image", "quantity", "price")
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
