from .cart import Cart
from .models import Category

def store_context(request):
    return {"nav_categories": Category.objects.all(), "cart_count": Cart(request).count}
