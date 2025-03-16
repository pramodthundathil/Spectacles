from django.shortcuts import render, redirect, get_object_or_404
from home.forms import UserAddForm, UserUpdateForm
from django.contrib import messages
from home.models import CustomUser
from .forms import ProductAddForm, ProductImageForm
from .models import Products, Category, Tax, Cart, CartItems
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.

# creating merchant from admin panel 

def merchants_admin(request):
    form = UserAddForm()
    merchant =  CustomUser.objects.filter(role = "merchant")

    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = "merchant"
            user.save()
            messages.success(request,"merchant Saved.....")
            return redirect("merchants_admin")

    context = {
        "form":form,
        "merchant":merchant
    }
    return render(request,"admin/merchants.html",context)

def delete_merchant(request, pk):
    # user = CustomUser.objects.get(id = pk)
    user = get_object_or_404(CustomUser, id= pk)
    user.delete()
    messages.success(request,"Merchant deleted")
    return redirect("merchants_admin")


def edit_merchant(request,pk):
    user = get_object_or_404(CustomUser, id = pk)
    form = UserUpdateForm(instance = user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,"Merchant deleted")
            return redirect("merchants_admin")

    context = {
        "form":form
    }
    return render(request,"admin/edit_merchant.html",context)



def products_merchant(request):
    products = Products.objects.filter(merchant = request.user)
    form = ProductAddForm()
    if request.method == "POST":
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.merchant = request.user
            product.save()
            messages.success(request,"Product added To List")
            return redirect("products_merchant")

    context = {
        "form":form,
        "products":products
    }
    return render(request,"merchant/products.html",context)


# def edit_product(request, pk):
#     product = Products.objects.get(id = pk)
#     product = get_object_or_404(Products, id = pk)

#     if request.method == "POST":
#         name = request.POST.get("name")
#         price = request.POST.get("price")
#         stock = request.POST.get("stock")
#         description = request.POST.get('dis')
#         img = None
#         if request.FILES:
#             img = request.FILES['image']

#         product.name = name 
#         product.price = price
#         product.stock = stock
#         product.description = description
#         if img:
#             product.image.delete()
#             product.image = img

#         product.save()
#         messages.success(request,"product Updated...")
#         return redirect(edit_product,pk = pk)

#     context = {
#         "product":product
#     }
#     return render(request,"merchant/edit_product.html",context)


def edit_product(request, pk):
    product = Products.objects.get(id = pk)
    product = get_object_or_404(Products, id = pk)
    image_form = ProductImageForm()
    form = ProductAddForm(instance=product)
    if request.method == "POST":
        form = ProductAddForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            product.save()
            messages.success(request,"product Updated...")
            return redirect(edit_product,pk = pk)

    context = {
        "form":form,
        "image_form":image_form,
        "product":product
    }
    return render(request,"merchant/edit_product.html",context)


def delete_product(request, pk):
    item  = get_object_or_404(Products, id= pk)
    item.delete()
    return redirect("products_merchant")


def add_images(request,pk):
    product = get_object_or_404(Products, id = pk)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.info(request,"Images Updated")
            return redirect(edit_product, pk = pk)

    return redirect(edit_product, pk = pk)


def category(request):
    categories = Category.objects.all()
    if request.method == "POST":
        cat = request.POST.get("cat")
        category1 = Category.objects.create(name = cat)
        category1.save()
        messages.success(request, "Category Added.....")
        return redirect(category)

    context = {
        "categories":categories
    }


    return render(request,"admin/category.html",context)





#cart functionalities

def cart(request):
    carts = get_object_or_404(Cart, user = request.user)

    context = {
        "carts":carts
    }
    return render(request,"cart.html",context)

def add_to_cart(request, pk):
    product = get_object_or_404(Products, id = pk)
    try:
        carts = get_object_or_404(Cart, user = request.user)
    except:
        carts = Cart.objects.create(user = request.user)
        carts.save()
    if CartItems.objects.filter(cart = carts, product = product).exists():
        cart_item = CartItems.objects.filter(cart = carts, product = product).first()
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItems.objects.create(cart = carts, product = product)
        cart_item.save()
    return redirect("cart")

def delete_cart_item(request, pk):
    CartItems.objects.get(id = pk).delete()
    messages.info(request,"Cart is deleted......")
    return redirect("cart")



def update_cart(request):
    if request.method == "POST":
        cart_item_id = request.POST["cart_item_id"]
        action = request.POST['action']
        cart_item = CartItems.objects.get(id = cart_item_id)

        carts = cart_item.cart
        html_page = render_to_string("ajax/cart_items.html",{"carts":carts})

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()

        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

            else:
                cart_item.delete()
        else:
            pass

        return JsonResponse({"success":True,"html":html_page})
    
    return JsonResponse({"success":True,"html":html_page})


from .models import Order, OrderItems

def order_creation(request):
    cat = Cart.objects.get(user = request.user)
    if CartItems.objects.filter(cart = cat).exists():

        order = Order.objects.create(user = request.user)
        order.save()
        cart = get_object_or_404(Cart, user = request.user)
        cart_items = cart.user_cart.all()
        for item in cart_items:
            print(item.product, item.quantity)
            if item.product.stock < item.quantity:
                messages.info(request, f"{item.product}- product is out of stock")
                return redirect("cart")
            else:
                order_item = OrderItems(order = order,product = item.product,quantity = item.quantity )
                order_item.save()
                item.delete()
            
        # order.update_totals()
        messages.info(request,"Order Was Created.. Please Pay the Amount....")
        return redirect("Payment_screen",pk = order.id)
    else:
        messages.info(request,"Cart was empty")
        return redirect("cart")


def add_to_order(request, item_id):
    product = get_object_or_404(Products, id = item_id)
    order_item = OrderItems(order_id = 16,product = product,quantity = 1 )
    order_item.save()
    
    return redirect(Payment_screen,pk =16)


import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@csrf_exempt
def Payment_screen(request, pk):
    order_id = get_object_or_404(Order, id= pk)
    if request.method == "POST":
        data = {
                "amount": order_id.total_amount * 100,
                "currency": "INR",
                "payment_capture": "1"
            }
        order = razorpay_client.order.create(data)
        order_id.payment_order_id = order["id"]
        order_id.save()

        return JsonResponse({"order_id": order["id"], "amount": order_id.total_amount, "key": settings.RAZOR_KEY_ID})
    return render(request,"payment.html",{"order":order_id})


@csrf_exempt
def callback(request):
    if request.method == "POST":
        response_data = request.POST
        order_id = response_data.get("razorpay_order_id")
        payment_id = response_data.get("razorpay_payment_id")
        signature = response_data.get("razorpay_signature")

        # Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature(response_data)
            print(order_id)
            order = get_object_or_404(Order, payment_order_id = order_id )
            order.payment_status = True 
            order.save()
            print("Working........")
            return JsonResponse({"status": "success"})
            # return render(request,"success.html")

        except:
            return JsonResponse({"status": "failed"})
            
            # return render(request,"error.html")
            
            # return JsonResponse({"status": "failed"})

    return JsonResponse({"status": "error"})
     


def orders(request):
    orders = Order.objects.filter(user = request.user)
    context = {
        "orders":orders
    }
    return render(request,"orders.html",context)


def orders_merchant(request):
    order_items = OrderItems.objects.filter(product__merchant = request.user)
    print(order_items)
    context = {
        "order_items_s":order_items
    }
    return render(request,"merchant/order.html",context)



from django.shortcuts import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def  Generate_invoice(request, pk):
    try:
        order = get_object_or_404(Order, id = pk) 
        order_items = order.order_items.all()
        context = {
            "order_items":order_items
        }
        # Render HTML template to string
        html = render_to_string('Invoice.html', context)

        # Generate the PDF from HTML
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice{order.order_number}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Check for errors
        if pisa_status.err:
            return HttpResponse("An error occurred while generating the PDF", status=500)
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



def chat(request):
    return render(request,"chat_with_merchant.html")