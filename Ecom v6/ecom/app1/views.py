from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from app1.models import product,cart,CartItem,Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    k = product.objects.all()
    cat = Category.objects.all()
    return render(request,'home.html',{"pro":k,"cat":cat})
def login1(request):
    if(request.method=="POST"):
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name,password=password)
        if user:
            login(request,user)
            return home(request)
        else:
            return HttpResponse("User Not Found!!")
    return render(request,'login.html')
def logout1(request):
    logout(request)
    return login1(request)
def signup1(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        if request.method == 'POST':
            name=request.POST.get('name')
            email=request.POST.get('email')
            password=request.POST.get('password')
            cpassword=request.POST.get('cpassword')
            if name=='' or email=='' or password=='' or cpassword=='':
                print('All Fields must be entered')
                return redirect(signup1)
            if password==cpassword:
                if User.objects.filter(username=name,email=email).exists():
                    messages.info(request,'username already exists') 
                else:
                    new = User.objects.create_user(username=name,password=password,email=email)
                    new.set_password(password)
                    new.save()
                    return redirect(login1)
            else:
                print("Wrong password")
    return render(request,'signup.html')

@login_required(login_url='login')
def addcart(request,uid):
    pro = product.objects.get(id=uid)
    crt,created = cart.objects.get_or_create(user=request.user)
    cart_item,item_created = CartItem.objects.get_or_create(crt=crt,pro=pro)
    if not item_created:
        cart_item.quantity += 1
        cart_item.total_price = pro.product_price*cart_item.quantity
        cart_item.save()
    else:
        cart_item.total_price = pro.product_price*cart_item.quantity
        cart_item.save()
    return redirect('home')

@login_required(login_url='login')
def viewcart(request):
    try:
        crt = request.user.cart
    except:
        return HttpResponse('Empty cart')
    else:
        Cart = cart.objects.get(user=request.user)
        k = CartItem.objects.filter(crt=crt)
        Cart.grandtotal=0
        su = 0
        for i in k:
            su = su+i.total_price
        Cart.grandtotal=su
        Cart.save()
        return render(request,'cart.html',{"k":k,"j":Cart})

@login_required(login_url='login')
def removeitem(request,uid):
    pro = product.objects.get(id=uid)
    crt = cart.objects.get(user=request.user)
    item = CartItem.objects.get(crt=crt,pro=pro)
    item.delete()
    return redirect('viewcart')

def increment(request,uid):
    pro = product.objects.get(id=uid)
    crt = cart.objects.get(user=request.user)
    item = CartItem.objects.get(crt=crt,pro=pro)
    item.quantity+=1
    item.total_price = pro.product_price*item.quantity
    item.save()
    return redirect('viewcart')

def decrement(request,uid):
    pro = product.objects.get(id=uid)
    crt = cart.objects.get(user=request.user)
    item = CartItem.objects.get(crt=crt,pro=pro)
    if item.quantity>1:
        item.quantity-=1
        item.total_price = pro.product_price*item.quantity
        item.save()
    else:
        item.delete()
    return redirect('viewcart')
def pro_view(request,uid):
    k = product.objects.get(id=uid)
    return render(request,'proView.html',{"k":k})

def allProducts(request):
    p = Paginator(product.objects.all(),2)
    page = request.GET.get('page')
    pa = p.get_page(page)
    return render(request,'allProducts.html',{"k":pa})
def search(request):
    if request.method=="POST":
        key = request.POST.get('searchQuery')
        serRes = product.objects.filter(product_name__contains=key)
        c = serRes.count()
        return render(request,'allProducts.html',{"k":serRes,"c":c})
    
def catfilter(request,uid):
    cat = Category.objects.get(id=uid)
    pro = product.objects.filter(cate=cat)
    p = Paginator(pro,2)
    page = request.GET.get('page')
    pa = p.get_page(page)
    c = pro.count()
    return render(request,'allProducts.html',{"k":pa,"c":c})