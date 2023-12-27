from ast import Dict
from math import prod
from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import *

def BASE(request):
          
    return render(request,"base.html")

def HOME(request):

    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.filter(status="PUBLISH").order_by('-id')[:20]
    
    data = {
        'category':category,
        'product':product,
    }

    return render(request,"home.html", data)

def CONTACT(request):
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'category':category
    }
    return render(request,"contact.html",data)

def SHOP(request):

    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.filter(status="PUBLISH").order_by('-id')[:100]
    discount_product = Product.objects.filter(discount__gte=10).order_by('-id')[:10]
    data = {
        'category':category,
        'product':product,
        'disProduct':discount_product
    }

    return render(request,"shop-grid.html", data)

def DETAIL_PRODUCT(request,slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        category = Category.objects.get(id=product.first().category.id)
        relatedProduct = Product.objects.filter(category=category)[:20]
        # print(relatedProduct)
        data = {
            'product':product.first,
            'relatedProduct':relatedProduct
        }
        print(data)
        return render(request,"shop-details.html",data)
    else:
        return redirect('home')

@login_required
def CART(request):
    cart = Cart.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'cart':cart,
        'category':category
    }
    return render(request,"shop-cart.html",data)

@login_required
def CHECKOUT(request):
    cart = Cart.objects.filter(user=request.user)
    add = Address.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'cart':cart,
        'category':category,
        'add':add.first()
    }
    return render(request,"checkout.html",data)

def SEARCH(request):
    
    search = request.GET.get('search')
    category = request.GET.get('cat')
    data={
        'title':search
    }
    if search != None:
        data['product'] = Product.objects.filter(title__icontains=search)
    else:
        if category != None:
            cat = Category.objects.filter(id=category)
            if cat.exists():
                data['title'] = category=cat.first().title
                data['product'] = Product.objects.filter(category=cat.first())

    return render(request,'search.html',data)