from django.urls import path
from .views import *

urlpatterns = [
    path("",DashboardView.as_view(),name="dashboard"),
    path("create_category/",CreateCatView.as_view(),name="create_category"),
    path("update_category/<pk>",UpdateCategoryView.as_view(),name="update_category"),
    path("create_subcategory/",CreateSubCategoryView.as_view(),name="create_subcategory"),
    path("update_subcategory/<pk>",UpdateSubCategoryView.as_view(),name="update_subcategory"),
    path("show_catsubcat/",ListCategorySubCategoryView.as_view(),name="show_cat_subcat"),
    path("create_products/",CreateProductView.as_view(),name="create_product"),
    path("show_products/",ListProductView.as_view(),name="show_products"),
    path("update_products/<pk>",UpdateProductView.as_view(),name="update_products"),
    path("search_products/<int:id>",search_products,name="search_products"),
    path("sold_form/<int:id>",SoldFormView.as_view(),name="sold_form"),
    path("sold_products_view/<date>",view_sold_products,name="view_sold_products"),
    path("products_details/<pk>",DetailProductView.as_view(),name="products_details"),
    path("product_list_fun/",list_products_view,name="function_products"),


]
