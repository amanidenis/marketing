from django.shortcuts import render
from store.models import Product  # Ensure correct import and class name

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)
