from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from .models import Tax , Products, OrderItems



@receiver(post_save, sender = Tax)
def update_product_on_tax_change(sender, instance, **kwargs):
    related_products = Products.objects.filter(tax_slab = instance )
    for product in related_products:
        product.save()

@receiver(post_delete, sender=Tax)
def update_product_on_tax_delete(sender, instance, **kwargs):
    related_products = Products.objects.filter(tax_slab=instance)
    for product in related_products:
        product.tax_slab = None  
        product.save() 

@receiver(post_save, sender=OrderItems)
def update_total_amount_on_order_item_add(sender, instance, **kwargs):
    order = instance.order
    order.update_totals()
    product = instance.product
    
    if product.stock < instance.quantity:
        instance.delete()
    else:
        
        product.stock -= instance.quantity
        product.save()

   

