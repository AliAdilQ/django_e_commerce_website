from django.urls import path
from . import views
app_name = "orders"
urlpatterns = [
    path("", views.order_list, name="list"), path("checkout/", views.checkout, name="checkout"),
    path("<uuid:reference>/", views.detail, name="detail"),
    path("<uuid:reference>/confirmation/", views.confirmation, name="confirmation"),
]
