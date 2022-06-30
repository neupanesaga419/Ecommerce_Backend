from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save, pre_delete,post_delete,pre_save



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
