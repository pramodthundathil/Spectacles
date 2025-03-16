from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_only
from merchant.models import Products, Tax


# # Create your views here.
# def signin(request):
#     return HttpResponse("<h1>App Is Working</h1>")

@admin_only
def index(request):
    products = Products.objects.all()[:4]

    context = {
        "products":products
    }
    return render(request,"index.html",context)

def admin_index(request):
    return render(request,"admin_index.html")

def merchant_index(request):
    return render(request,"merchant/merchant_index.html")


def products(request):
    product = Products.objects.all()

    context = {
        "products":product
    }
    return render(request,"products.html",context)


def virtual_try(request, pk):
    product = get_object_or_404(Products, id =pk)

    context = {
        "product":product
    }
    return render(request,"virtual_try.html",context)

from django.core.files.storage import default_storage
from .sunglass import glass_Analyse

def virtual(request, pk):
    product = get_object_or_404(Products, id =pk)
    try:
        with default_storage.open(product.virtual_product.name, 'rb') as file:
            glass_Analyse(file)
            print("--------Company successful")
    except Exception as e:
        messages.error(request, "Something Wrong")
        return redirect("virtual_try", pk =  pk)

    return redirect("virtual_try", pk =  pk)

def signin(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        user = authenticate(request, username = uname, password = pswd)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request,"Username or password incorrect")
            return redirect("signin")
        print(uname, pswd,"-------------------------------------------")
    return render(request, 'login.html')


def signup(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Registered Success....")
            return redirect("signin")
        else:
            messages.error(request,form.errors)
            return redirect("signup")
        
    context = {
        "form":form
    }
    return render(request,'register.html',context)

def signout(request):
    logout(request)
    return redirect(signin)



def tax_mgt(request):
    taxs = Tax.objects.all()
    if request.method == "POST":
        tax_name = request.POST.get("tax_name")
        tax_value = request.POST.get("tax_value")

        tax = Tax.objects.create(tax_name  = tax_name, tax_value = tax_value )
        tax.save()

        messages.success(request,"Tax Value Saved")
        return redirect("tax_mgt")


    context = {
        "taxs":taxs
    }
    return render(request,"admin/tax.html",context)


def edit_tax(request, pk):
    tax = get_object_or_404(Tax, id = pk)

    if request.method == "POST":
        tax_name = request.POST.get("tax_name")
        tax_value = request.POST.get("tax_value")

        tax.tax_name = tax_name
        tax.tax_value = tax_value

        tax.save()
        messages.success(request,"Tax, Value Updated.....")
        return redirect(tax_mgt)

    context = {
        "tax":tax
    }
    return render(request,"admin/update_tax.html",context)


def delete_tax(request, pk):
    Tax.objects.get(id = pk).delete()
    messages.success(request,"Tax, Value Updated.....")
    return redirect(tax_mgt)


from .models import CustomUser, Chat_Messages

def chat_user_list(request):
    users = CustomUser.objects.all()
    context = {
        "users":users
    }
    return render(request,"chat_user_list.html",context)


def chat_view(request, user_id):
    """ Load the chat interface between two users. """
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.user.id == other_user.id:
        import django.contrib.messages
        django.contrib.messages.info(request,"You Cannot sent Self message ")
        return redirect("index")

    # Fetch previous messages between two users
    messages = Chat_Messages.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("created_at")

    return render(request, "chat_with_merchant.html", {"messages": messages, "other_user": other_user})



def chat_list_merchant(request):
    users = CustomUser.objects.all()
    context = {
        "users":users
    }
    return render(request,"merchant/chat_user_list.html",context)

def chat_with_user(request, user_id):
    
    """ Load the chat interface between two users. """
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.user.id == other_user.id:
        import django.contrib.messages
        django.contrib.messages.info(request,"You Cannot sent Self message ")
        return redirect("index")

    # Fetch previous messages between two users
    messages = Chat_Messages.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("created_at")

    return render(request, "chat_with_user.html", {"messages": messages, "other_user": other_user})


def user_profile_update(request):
    user = request.user

    form = UserUpdateForm(instance = user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,"User Update Success....")
            return redirect("user_profile_update")
        else:
            messages.error(request,form.errors)
            return redirect("user_profile_update")

    context = {
        "form":form
    }
    return render(request,"profile_page.html",context)