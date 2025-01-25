from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Product

# Create your views here.


def store(request):
    return render(request, 'store/store.html')


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}