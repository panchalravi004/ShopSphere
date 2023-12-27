from datetime import date
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.EmailBackEnd import EmailBackEnd
from app.models import *
from app.templatetags.filterData import cartTotal


def REGISTER(request):

    return render(request,"registration/registration.html")

def LOGIN(request):
    referer_url = request.META.get('HTTP_REFERER', '/default-url/')
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('pass')
        user = EmailBackEnd.authenticate(request,username=email,password=pwd)

        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email and Password Are Invalid !')
            return redirect('login')

    messages.warning(request,'Invalid request method !')
    return redirect(referer_url)

def CREATEACCOUNT(request):

    referer_url = request.META.get('HTTP_REFERER', '/default-url/')

    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('pass')
        re_pwd = request.POST.get('re_pass')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = "{}{}".format(fname,lname)

        if pwd != re_pwd:
            messages.warning(request,'Password does not match !')
            return redirect(referer_url)

        user = User(
            username=uname,
            first_name=fname,
            last_name=lname,
            email=email,
        )
        user.set_password(pwd)
        user.save()

        # messages.success(request,'Email and Password Are Invalid !')
        return redirect('login')
    
    messages.warning(request,'Invalid request method !')
    return redirect(referer_url)

@login_required
def ADDCART(request):
    id = request.GET.get('id')
    qty = request.GET.get('qty')
    product = Product.objects.filter(id=id)

    if product.exists():
        check = Cart.objects.filter(user=request.user,product=product.first())
        if check.exists():
            cart = check.first()
            cart.quantity=check.first().quantity + int(qty)
            cart.save()
            return redirect('cart')
        else:
            cart = Cart(
                user=request.user,
                quantity=qty,
                product=product.first(),
            )
            cart.save()
            return redirect('cart')
    else:
        messages.warning(request,"Product is not exists !")
        return redirect('home')
    
@login_required
def REMOVECART(request,id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect('cart')

@login_required
def UPDATEQTY(request,action,id):
    if action == 'add':
        cart = Cart.objects.get(id=id)
        cart.quantity = cart.quantity + 1
        cart.save()    
    else:
        cart = Cart.objects.get(id=id)
        if cart.quantity == 1:
            cart.delete()
        else:
            cart.quantity = cart.quantity - 1
            cart.save()
    return redirect('cart')

@login_required
def LOGOUT(request):
    logout(request)
    return redirect('login')

@login_required
def PROFILE(request):
    add = Address.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'add':add.first(),
        'category':category
    }
    
    return render(request,'profile.html',data)

@login_required
def PROFILEUPDATE(request):
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd = request.POST.get('pass')

        userid = request.user.id
        user = User.objects.get(id=userid)
        user.email = email
        user.first_name = fname
        user.last_name = lname

        if pwd != None and pwd != "":
            user.set_password(pwd)
        user.save()

        address = Address.objects.filter(user=request.user)

        if address.exists():
            address = address.first()
            address.street = request.POST.get('street')
            address.pin = request.POST.get('pin')
            address.subdistrict = request.POST.get('subdistrict')
            address.district = request.POST.get('district')
            address.state = request.POST.get('state')
            address.save()
        else:
            address = Address(
                user = request.user,
                street = request.POST.get('street'),
                pin = request.POST.get('pin'),
                subdistrict = request.POST.get('subdistrict'),
                district = request.POST.get('district'),
                state = request.POST.get('state')
            )
            address.save()

    return redirect('profile')

@login_required
def ORDER(request):
    order = Order.objects.filter(user=request.user).order_by('-orderdate')
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'order':order,
        'category':category
    }
    return render(request,"shop-order.html", data)

@login_required
def CREATEORDER(request):
    cart = Cart.objects.filter(user=request.user)
    total = cartTotal(cart)
    shipdate = date.today()
    if int(str(date.today())[8:]) > 23:
        shipdate = str(date.today())[0:7]+"-"+str(int(str(date.today())[8:]) + 7 - 30)
    else:
        shipdate = str(date.today())[0:7]+"-"+str(int(str(date.today())[8:]) + 7)
    print(shipdate)
    
    order = Order(
        user=request.user,
        total=total,
        shipdate=shipdate,
        status='PENDING',
    )

    order.save()

    for c in cart:
        item = OrderItem(
            order=order,
            product=c.product,
            total=int(c.product.price) * int(c.quantity),
            quantity=c.quantity
        )
        item.save()
    for c in cart:
        c.delete()
    
    return redirect('order')

