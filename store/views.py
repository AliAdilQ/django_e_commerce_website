from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, DecimalField, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartQuantityForm, NewsletterForm
from .models import Category, NewsletterSubscriber, Product


def home(request):
    products = Product.objects.filter(available=True).select_related("category")
    return render(request, "store/home.html", {
        "featured_products": products.filter(featured=True).order_by("id")[:8],
        "latest_products": products[:4],
        "categories": Category.objects.annotate(product_count=Count("products", filter=Q(products__available=True))).order_by("id"),
    })


def shop(request, category_slug=None):
    products = Product.objects.filter(available=True).select_related("category")
    category = None
    selected = category_slug or request.GET.get("category", "")
    if selected:
        category = get_object_or_404(Category, slug=selected)
        products = products.filter(category=category)
    query = request.GET.get("q", "").strip()[:200]
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))
    if request.GET.get("sale") == "1":
        products = products.filter(discount_price__isnull=False)
    if request.GET.get("stock") == "1":
        products = products.filter(stock__gt=0)
    sort = request.GET.get("sort", "newest")
    ordering = {"newest": "-created_at", "price_asc": "selling_price", "price_desc": "-selling_price", "name": "name"}
    if sort not in ordering:
        sort = "newest"
    products = products.annotate(selling_price=Coalesce("discount_price", "price", output_field=DecimalField())).order_by(ordering[sort], "id")
    page = Paginator(products, 12).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "store/shop.html", {
        "page_obj": page, "category": category, "query": query, "sort": sort,
        "filter_query": params.urlencode(), "sale_only": request.GET.get("sale") == "1",
        "stock_only": request.GET.get("stock") == "1",
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, available=True)
    related = Product.objects.filter(category=product.category, available=True).exclude(pk=product.pk)[:4]
    return render(request, "store/product_detail.html", {"product": product, "related_products": related})


def cart_detail(request):
    cart = Cart(request)
    items = cart.items()
    return render(request, "store/cart.html", {"items": items, "total": cart.total,
                                              "has_stock_error": any(item["stock_error"] for item in items)})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)
    form = CartQuantityForm(request.POST)
    if form.is_valid():
        try:
            Cart(request).add(product, form.cleaned_data["quantity"])
            messages.success(request, f"{product.name} added to your bag.")
        except ValueError as error:
            messages.error(request, str(error))
    else:
        messages.error(request, "Choose a valid quantity between 1 and 999.")
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(next_url)
    return redirect("store:cart")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = CartQuantityForm(request.POST)
    if form.is_valid():
        try:
            Cart(request).add(product, form.cleaned_data["quantity"], replace=True)
            messages.success(request, "Your bag has been updated.")
        except ValueError as error:
            messages.error(request, str(error))
    else:
        messages.error(request, "Choose a valid quantity between 1 and 999.")
    return redirect("store:cart")


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove(product_id)
    messages.success(request, "Item removed from your bag.")
    return redirect("store:cart")


@require_POST
def newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        _, created = NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data["email"].lower())
        messages.success(request, "You're on the list! This demo stores your subscription locally; no emails are sent." if created else "You're already on the list. Thanks for being here!")
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(reverse("store:home") + "#newsletter")


def about(request):
    return render(request, "store/about.html")


def support(request):
    return render(request, "store/support.html")
