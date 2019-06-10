from django import forms
from django.forms import FileField

from .models import Product


class PostForm(forms.ModelForm):
    image_url = forms.FileField(required=True,label="Image")

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'image_url']