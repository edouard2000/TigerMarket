from django.shortcuts import render
from .models import Product

def store(request):
    products = Product.objects.filter(is_available=True)
    products_counts = products.count()
    context = {
        "products": products,
        "products_counts": products_counts
    }
    return render(request, 'store/store.html', context)
