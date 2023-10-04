from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from app1.models import product,cart,CartItem
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    k = product.objects.all()
    return render(request,'home.html',{"pro":k})
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
            if password==cpassword:
                if User.objects.filter(username=name,email=email).exists():
                    messages.info(request,'usename already exists')
                    print('Already have')
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
        cart_item.quantity+=1
        cart_item.save()
    return redirect('home')

@login_required(login_url='login')
def viewcart(request):
    try:
        crt = request.user.cart
    except:
        return HttpResponse('Empty cart')
    else:
        k = CartItem.objects.filter(crt=crt)
        return render(request,'cart.html',{"k":k})

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
    item.save()
    return redirect('viewcart')

def decrement(request,uid):
    pro = product.objects.get(id=uid)
    crt = cart.objects.get(user=request.user)
    item = CartItem.objects.get(crt=crt,pro=pro)
    if item.quantity>1:
        item.quantity-=1
        item.save()
    else:
        item.delete()
    return redirect('viewcart')