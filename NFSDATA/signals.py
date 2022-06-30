from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save, pre_delete,post_delete,pre_save
from django import forms


# For Product
@receiver(post_delete,sender=Products)
def post_delete_Teacher(sender,instance,*args,**kwargs):
    
    try:
        instance.product_image.delete(save=False)
    except:
        pass
    
@receiver(pre_save,sender=Products)
def pre_save_Teacher(sender,instance,*args,**kwargs):
    
    try:
        print("yess")
        old_data = instance.__class__.objects.get(id=instance.id).product_image.path
        try:
            new_data = instance.product_image.path
        except:
            new_data = old_data
        if new_data!=old_data:
            import os 
            if os.path.exists(old_data):
                os.remove(old_data)
            
    except:
        pass


@receiver(pre_save,sender=SoldProducts)
def pre_save_products_amount(sender,instance,*args,**kwargs):
    try:
        sold_product = instance.__class__.objects.get(id=instance.id)
        amount_sold_before_edit = sold_product.product_amount_sold        
        sold_product_id = sold_product.product_sold.id
        product = Products.objects.get(id=sold_product_id)
        amount_present = product.product_amount

        try:
            amount_sold_after_edit = instance.product_amount_sold
        except:
            new_value = old_value  
        
        if amount_sold_after_edit != amount_sold_before_edit:
            amount_changed = amount_sold_after_edit - amount_sold_before_edit
            # print(amount_changed)
            
            if amount_changed > amount_present:
                raise forms.ValidationError("You Have Entered More Amount than that present in Database")
            
            else:
                amount_present_now = amount_present - amount_changed
                product.product_amount = amount_present_now
                product.save()

    except:
        pass
