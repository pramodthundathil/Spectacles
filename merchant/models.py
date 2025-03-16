from django.db import models
from home.models import CustomUser


# tax - 0% , 5%, 12%, 18%

class Tax(models.Model):
    tax_name = models.CharField(max_length=20, help_text='Name Of the Tax (eg: VAT, GST etc.)')
    tax_value = models.FloatField(help_text="Tax Value in Percentage(%)")


    def __str__(self):
        return self.tax_name + " - " +str(self.tax_value)
    

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

 
class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products",null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")

    virtual_product  =  models.ImageField(upload_to="virtual_image", null=True, blank=True)

    tax_slab = models.ForeignKey(Tax, on_delete=models.SET_NULL,null=True, blank=True)
    tax = models.FloatField(default=0)

    price_before_tax = models.FloatField(default=0)
    price_after_tax = models.FloatField(default=0)


    def save(self,*args,**kwargs):
        try:
            tax_value = self.tax_slab.tax_value
        except:
            tax_value = 0
        price = self.price
        self.price_before_tax = price
        tax = (price * tax_value) / 100
        self.tax = tax
        self.price_after_tax = self.price_before_tax + self.tax
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="product_image")
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImages.objects.filter(product = self.product, is_primary = True).update(is_primary = False)

        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.product.name} - {'Primary' if self.is_primary else 'Secondary'}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE )
    cart_total_price  = models.FloatField(default=0)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="user_cart")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()


    def save(self, *args, **kwargs):

        price = self.product.price
        self.price = price * self.quantity
        super().save(*args, **kwargs)




    def __str__(self):
        return self.product.name
    


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="checkout")
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    total_amount = models.FloatField(default=0)
    total_tax = models.FloatField(default=0)
    total_amount_before_tax = models.FloatField(default=0)
    check_out_status = models.BooleanField(default= True)
    payment_status = models.BooleanField(default=False)
    order_number = models.CharField(max_length=20)
    payment_order_id = models.CharField(max_length=100,null=True, blank=True )
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES, default='PENDING')

    def update_totals(self):
        order_items = self.order_items.all()
        total_price = 0
        total_tax = 0
        for item in order_items:
            total_price += item.total_price
            total_tax += item.total_tax
        
        self.total_amount_before_tax = total_price - total_tax
        self.total_amount = total_price
        self.total_tax = total_tax
        self.save()
            
    def save(self, *args, **kwargs ):
        if not self.order_number:
            # prev_order = Order.objects.last()
            try:
                prev_order = Order.objects.all().order_by("id").last()
                prev_order_id = prev_order.id
                order_number = int(prev_order_id) + 1
                self.order_number = f"OR-{order_number}"
            except:
                self.order_number = "OR-1"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} - Order {self.order_number}"
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Products, models.CASCADE)
    quantity = models.FloatField(default=1)
    total_price = models.FloatField(default=0)
    total_tax = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        price = self.product.price
        self.total_price = price * self.quantity
        self.total_tax = self.product.tax * self.quantity
        
        super().save(*args, **kwargs)


    

