from django.urls import path
from . import views
app_name = "store"
urlpatterns = [
    path("", views.home, name="home"), path("shop/", views.shop, name="shop"),
    path("search/", views.shop, name="search"),
    path("category/<slug:category_slug>/", views.shop, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("about/", views.about, name="about"), path("support/", views.support, name="support"),
]
