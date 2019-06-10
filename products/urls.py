from django.urls import path
from .views import ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from . import views
urlpatterns = [
    path('', views.index,name='shop-home'),
    # path('cart/' , views.cart,name='shop-cart'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('result/', views.search, name='search')

]
