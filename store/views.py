from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(categorry=category, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        products_count = products.count()

    context = {
        "products": products,
        "products_count": products_count,
    }
    return render(request, 'store/store.html', context)
