from django.db import models
from .formatchecker import ContentRestrictiononFileField
# from nepali_datetime_field.models import NepaliDateField
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    cateogry_details = models.TextField()
    created_on =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    sub_cat_name = models.CharField(max_length=255)
    sub_cat_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sub_cat_name


class SizeCategory(models.Model):
    size_name = models.CharField(max_length=50)
    size_code = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.size_code

class Brands(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.brand_name
      

GENDER = (("MALE","MALE"),("FEMALE","FEMALE"),("OTHERS","OTHERS"))
AGE_GROUPS = (("INFANTS","Below 5"),("MID_INFANTS","6-15"),("TEENAGER","16-24"),("WORKING","25-55"),("DEPENDENTS","Over 56"))



class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_amount = models.IntegerField(validators=[MinValueValidator(0),])
    product_cost_price = models.FloatField(validators=[MinValueValidator(0.0),])
    product_image = ContentRestrictiononFileField(
        upload_to = "products/",
        default=None,
        max_upload_size=2500000,
        content_types = ["image/jpeg","image/png","image/JPG","image/jpg"],
                                                  )
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,default="No Category")
    product_subcategory =  models.ForeignKey(SubCategory, on_delete=models.SET_NULL,null=True,default="NO Sub Category")
    product_gender = models.CharField(choices=GENDER,max_length=20)
    product_age_groups = models.CharField(choices=AGE_GROUPS,max_length=30)
    product_brand = models.ForeignKey(Brands, default=None,on_delete=models.SET_NULL,null=True)
    product_size = models.ManyToManyField(SizeCategory)
    product_minicategory = models.CharField(max_length=100,default=None,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    date_added = models.DateField()
    
    def product_size_availiable(self):
        return [str(item) for item in self.product_size.all()]

    def sold(self,product_amount_sold):
        self.product_amount = self.product_amount - product_amount_sold
    
    def cost_item(self):
        return self.product_amount * self.product_cost_price
    
    def __str__(self):
        return self.product_name
    
class SoldProducts(models.Model):
    product_sold = models.ForeignKey(Products, on_delete=models.SET_DEFAULT,null=True,default="Sold Item")
    product_selling_price = models.FloatField(validators=[MinValueValidator(0.0),])
    product_amount_sold = models.IntegerField(validators=[MinValueValidator(0),])
    created_on = models.DateTimeField(auto_now_add=True)
    added_date = models.DateField()
    
    def total_on_each_item(self):
        return self.product_selling_price * self.product_amount_sold
    
    def profit_or_loss_per_piece(self):
        cost_price = self.product_sold.product_cost_price
        selling_price = self.product_selling_price
        profit_or_loss = selling_price - cost_price
        return profit_or_loss
    
    def total_profit_or_loss(self):
        profit_or_loss = self.profit_or_loss_per_piece()
        return profit_or_loss * self.product_amount_sold
    
    
    
    def __str__(self):
        return self.product_sold.product_name


        
