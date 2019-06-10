from django.conf.urls import url

from .views import add_to_cart, order_details
urlpatterns = [
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', order_details, name="cart_summary")
]