from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product
from users.models import Profile,User
from .models import OrderItem,Order
from django.utils import timezone


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.eproduct.all():
        messages.info(request, 'You already own this product')
        return redirect('shop-home')


    if product.uploader==request.user:
        messages.info(request, 'You already own this product')
        return redirect('shop-home')
        # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect('shop-home')


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'cart_summary.html', context)


@login_required()
def delete_from_cart(request, item_id):
    item_id=int(item_id)
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if OrderItem.product == item_id:
        print('yes')
    else:
      print('no')
    try:
        i=OrderItem.objects.get(pk=8)
        print(i.id)

    except ObjectDoesNotExist:
        print("not exists")

    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('cart_summary')