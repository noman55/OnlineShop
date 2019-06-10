from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import generic

from .models import Product
from django.contrib import messages
from .form import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products': products})


# def cart(request):
#     return render(request,'cart.html')


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class=PostForm
    '''
    model = Product
    fields = ['name', 'price', 'stock', 'image_url']
    '''
    success_url = reverse_lazy('shop-home')
    template_name='products/product_form.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    template_name = 'products/product_form.html'
    model = Product
    '''
    model = Product
    fields = ['title', 'content']
    '''
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.uploader:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/products/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.uploader:
            return True
        return False
# function view


def upload_product(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.uploader=request.user
            messages.info(request,'successfully created post')
            return redirect('shop-home')
    else:
        form = PostForm()
    return render(request, 'products/product_form.html', {
        'form': form
})


def search(request):
    template='index.html'
    query=request.GET.get('q')
    results=Product.objects.filter(Q(name__icontains=query))
    # results=results.objects.all()
    return render(request,'index.html', {'products': results})