from django.urls import path 
from .import views 
from .api import views as api_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [

    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("",views.index,name="index"),
    path("signout",views.signout,name="signout"),
    path("admin_index",views.admin_index,name="admin_index"),
    path("merchant_index",views.merchant_index,name="merchant_index"),
    path("tax_mgt",views.tax_mgt,name="tax_mgt"),
    path("edit_tax/<int:pk>",views.edit_tax, name="edit_tax"),
    path("delete_tax/<int:pk>",views.delete_tax,name="delete_tax"),
    path("chat_user_list",views.chat_user_list,name="chat_user_list"),
    path("chat_view/<int:user_id>",views.chat_view,name="chat_view"),
    path("chat_with_user/<int:user_id>",views.chat_with_user,name="chat_with_user"),
    path("chat_list_merchant", views.chat_list_merchant, name="chat_list_merchant"),
    path("user_profile_update",views.user_profile_update,name="user_profile_update"),
    path("products",views.products,name= "products"),
    path("virtual_try/<int:pk>",views.virtual_try,name="virtual_try"),
    path("virtual/<int:pk>",views.virtual,name="virtual"),

    # api urls 

    path("demo_data/",api_view.demo_data, name="demo_data"),
    path("product_list/",api_view.product_list,name="product_list"),
    path("product_single/<int:pk>/",api_view.product_single,name="product_single"),
    path("product_single_with_id/",api_view.product_single_with_id,name="product_single_with_id"),
    path("create_product/",api_view.create_product,name="create_product"),
    path("delete_product/",api_view.delete_product,name="delete_product"),

    path("api/token/",api_view.MyTokenObtainPairView.as_view(),name="api/token/")


]


router.register(r"product", api_view.ProductViewset, basename='product')

urlpatterns += router.urls