from django.shortcuts import render, get_object_or_404
from .models import Product  # Import the Product model
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Helper function to get the shared context
def get_shared_context():
    categories = Category.objects.all()
    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 3) 
    page = 1  # Default page or you can modify as needed
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    return {
        'categories': categories,
        'products': paged_products,
        'product_count': product_count,
    }

def store(request, category_slug=None):
    categories = Category.objects.all()
    products = None

    if category_slug is not None:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=selected_category, is_available=True)
        paginator = Paginator(products, 1)  # Use Paginator class instead of variable name Paginator
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3) 
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'categories': categories,
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)





def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
   
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }      
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q( product_name__icontains=keyword))
            product_count = products.count()    

    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)





