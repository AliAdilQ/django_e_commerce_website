import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from store.cart import Cart
from .forms import CheckoutForm
from .models import Order
from .services import CheckoutError, place_order


@login_required
def checkout(request):
    cart = Cart(request)
    # A repeated submission resolves to its existing order before checking the empty cart.
    if request.method == "POST":
        try:
            posted_token = uuid.UUID(request.POST.get("checkout_token", ""))
        except (ValueError, AttributeError):
            posted_token = None
        if posted_token:
            existing = Order.objects.filter(user=request.user, checkout_token=posted_token).first()
            if existing:
                return redirect("orders:confirmation", reference=existing.reference)
    items = cart.items()
    if not items:
        messages.info(request, "Your bag is empty. Find your next favorite in the shop.")
        return redirect("store:shop")
    token = request.session.setdefault("checkout_token", str(uuid.uuid4()))
    form = CheckoutForm(request.POST if request.method == "POST" else None, initial={
        "full_name": request.user.get_full_name(), "email": request.user.email,
        "country": "Indonesia", "payment_method": "cod", "checkout_token": token,
    })
    if request.method == "POST" and form.is_valid():
        if str(form.cleaned_data["checkout_token"]) != token:
            form.add_error(None, "This checkout has expired. Reload the page and try again.")
        else:
            try:
                order = place_order(request.user, cart.data, form.cleaned_data)
            except CheckoutError as error:
                form.add_error(None, str(error))
            else:
                cart.clear()
                request.session.pop("checkout_token", None)
                messages.success(request, "Order placed! Thanks for shopping with NovaShop.")
                return redirect("orders:confirmation", reference=order.reference)
    return render(request, "orders/checkout.html", {"form": form, "items": items, "total": cart.total})


@login_required
def order_list(request):
    page = Paginator(Order.objects.filter(user=request.user), 10).get_page(request.GET.get("page"))
    return render(request, "orders/list.html", {"page_obj": page})


@login_required
def detail(request, reference):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), reference=reference, user=request.user)
    return render(request, "orders/detail.html", {"order": order})


@login_required
def confirmation(request, reference):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), reference=reference, user=request.user)
    return render(request, "orders/confirmation.html", {"order": order})
