from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Product
from django.shortcuts import get_object_or_404
# Create your views here.


def store(request):
    all_products = Product.objects.all()
    return render(request, 'store/store.html', dict(all_products=all_products))


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


def category_list(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', dict(category=category, products=products))


def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product-info.html', dict(product=product))