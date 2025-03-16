from django.urls import path 
from .import views 

urlpatterns = [
    path("merchants_admin",views.merchants_admin,name="merchants_admin"),
    path("delete_merchant/<int:pk>",views.delete_merchant,name="delete_merchant"),
    path("edit_merchant/<int:pk>",views.edit_merchant,name="edit_merchant"),
    path("products_merchant",views.products_merchant,name="products_merchant"),
    path("edit_product/<int:pk>",views.edit_product,name="edit_product"),
    path("category",views.category,name="category"),
    path("add_images/<int:pk>",views.add_images,name="add_images"),
    path("cart",views.cart,name="cart"),
    path("add_to_cart/<int:pk>",views.add_to_cart,name="add_to_cart"),
    path("delete_cart_item/<int:pk>",views.delete_cart_item, name="delete_cart_item"),
    path("update_cart",views.update_cart,name="update_cart"),
    path("delete_product/<int:pk>",views.delete_product, name="delete_product"),



    path("order_creation",views.order_creation,name="order_creation"),
    path("Payment_screen/<int:pk>",views.Payment_screen,name="Payment_screen"),
    path("add_to_order/<int:item_id>",views.add_to_order,name="add_to_order"),
    path("callback/", views.callback, name="callback"),
    path("orders",views.orders,name="orders"),
    path("orders_merchant",views.orders_merchant,name="orders_merchant"),
    path("Generate_invoice/<int:pk>",views.Generate_invoice,name="Generate_invoice"),
    path("chat",views.chat,name="chat"),
]