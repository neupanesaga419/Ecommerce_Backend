from django.contrib import admin
from .models import *
from django.urls import reverse_lazy


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_name','cateogry_details']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id","sub_cat_name","sub_cat_details"]


@admin.register(SizeCategory)
class SizeCategoryAdmin(admin.ModelAdmin):
    list_display = ["id","size_name","size_code","created_on"]
    
@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ["id","brand_name","brand_details","created_on"]

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "product_name",
                    "product_amount",
                    "product_cost_price",
                    "product_image",
                    "product_category",
                    "product_subcategory",
                    "product_gender",
                    "product_age_groups",
                    "product_brand",
                    "product_minicategory",
                    "product_size_availiable",
                    "date_added"
                    
                    ]

@admin.register(SoldProducts)
class SoldProductsAdmin(admin.ModelAdmin):
    list_display = ["id","product_sold","product_selling_price","product_amount_sold","created_on","added_date"]

admin.site.site_title = "NFS ADMIN"
admin.site.site_header = "NFS ADMIN"