from django.shortcuts import render,redirect,Http404
from django.views.generic import CreateView,DeleteView,UpdateView
from django.views.generic import ListView,DetailView,TemplateView,FormView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
import json
from .helpers import week_day_sales,find_item_n_amount,seven_back_days_generator
import NFSDATA.helpers as hp
import NFSDATA.yearmonth as ym


@method_decorator(login_required(login_url="signin"),name="dispatch")
class DashboardView(TemplateView):
    from datetime import datetime,timedelta
    from datetime import date
    template_name = "pages/dashboard.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        seven_days,labels = seven_back_days_generator()
        num_prod_today = Products.objects.filter(date_added=seven_days[0]).count()
        num_prod_yesterday = Products.objects.filter(date_added=seven_days[1]).count()
        
        percentage_change_in_number_added_prod = round((num_prod_today - num_prod_yesterday)/(num_prod_today + num_prod_yesterday) * 100)

        if SoldProducts.objects.filter(added_date=seven_days[0]).exists():            
            most_sold_item,most_sold_item_amount = find_item_n_amount(SoldProducts,seven_days[0])
            
            total_sales_data = []
            total_profit_data = []
            
            for i in range(7):
                total_sold_on_day,total_profit_on_day = week_day_sales(SoldProducts,seven_days[i])
                total_sales_data.append(total_sold_on_day)
                total_profit_data.append(total_profit_on_day)
            
            # Converting Python Data into JSON DATA so that JavaScript Can Read it
            data_data = json.dumps(total_sales_data)
            data_profit = json.dumps(total_profit_data)
            datalabel = json.dumps(labels)
        
            total_sales_change = round(((total_sales_data[0] - total_sales_data[1]) / (total_sales_data[0] + total_sales_data[1]))*100)
            total_profit_change = round(((total_profit_data[0] - total_profit_data[1]) / (total_profit_data[0] + total_profit_data[1]))*100)
            loss = False
            if total_profit_change < 0:
                loss = True
                
            twelve_months,month_sort = ym.months_generator()
            monthly_sold_data,labelmonths = ym.get_total_sold_monthly(SoldProducts, twelve_months, month_sort)
            
            monthly_sold_data = json.dumps(monthly_sold_data)
            labelmonths = json.dumps(labelmonths)
            
            context["monthly_sold_data"] = monthly_sold_data
            context["labelmonths"] = labelmonths
            context ["loss"] = loss
            context["data"] = data_data 
            context["labels"] = datalabel
            context["profit"] = data_profit
            context["date_today"] = seven_days[0]
            context["date_before_seven"]= seven_days[6]
            context["products_added_today"] = num_prod_today
            context["percentage_change"] = percentage_change_in_number_added_prod
            context["most_sold_item"] = most_sold_item
            context["most_sold_item_amount"] = most_sold_item_amount
            context["total_sales_change"] = total_sales_change
            context["total_profit_change"] = total_profit_change
            context["total_sold"] = '{:,.2f}'.format(total_sales_data[0])
            context["total_profit"] = '{:,.2f}'.format(total_profit_data[0])
            context["total_item_sold"] = hp.total_item(SoldProducts,"product_amount_sold",seven_days[0])
        
            context["total_remainig_item"] = hp.total_item(Products, "product_amount")
            context["total_remaining_cost"] = '{:,.2f}'.format(hp.total_rem_cost(Products))
            
            context["total_item_sold_till_now"] = hp.total_item(SoldProducts, "product_amount_sold")
             
            total_sold_cost, total_profit_earned = hp.week_day_sales(SoldProducts)
            context["total_sold_cost_till_now"],context["total_profit_earned_till_now"] = 'Rs {:,.2f}'.format(total_sold_cost),'Rs {:,.2f}'.format(total_profit_earned)
            
            
            # MOST SOLD ITEMS
            item,amount = hp.find_item_n_amount(SoldProducts)
            context["most_sold_item_till_now"],context["most_sold_item_amount_till_now"] = item,amount
            context["most_sold_item_cost"] = "Rs {:,.2f}".format(item.product_cost_price)
            
            # MOST PROFIT Giving ITEMS
            most_profit_given_item,profit_given_by_item = hp.most_profit_given()
            context["most_profit_given_item"],context["profit_given_by_item"] = most_profit_given_item,"Rs {:,.2f}".format(profit_given_by_item)
            
            
            # Expensive and Costly Item
            expensive_item,costly_item = hp.most_expensive_costly()
            context["most_expensive_item"],context["most_costly_item"] = expensive_item,costly_item
            context["most_expensive_item_cost"],context["most_costly_item_cost"] = "Rs {:,.2f}".format(expensive_item.product_cost_price),"Rs {:,.2f}".format(costly_item.product_cost_price)
            
            sagar = hp.find_item_n_amount(SoldProducts,list_return=5)

            context["top_five_items"] = sagar
            context["date"] = self.datetime.today()

        else:
            context["product_found"] = False
        
        
        return context
    
    
    
    
# Create your views here.
@method_decorator(login_required(login_url="signin"),name="dispatch")
class CreateCatView(SuccessMessageMixin,CreateView):
    model = Category
    template_name = "pages/create_category.html"
    # fields = "__all__"
    form_class = CategoryForm
    success_url = reverse_lazy("show_cat_subcat")
    success_message = "New Category Has Been Added Successfully"
    
@method_decorator(login_required(login_url="signin"),name="dispatch")
class CreateSubCategoryView(SuccessMessageMixin,CreateView):
    model = SubCategory
    template_name = "pages/create_subcategory.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("show_cat_subcat")
    success_message = "New Sub Category Has Been Added Successfully"


@method_decorator(login_required(login_url="signin"),name="dispatch")
class ListCategorySubCategoryView(ListView):
    model = Category
    template_name = "pages/tables.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(ListCategorySubCategoryView,self).get_context_data(**kwargs)
        context["subcategory_list"] = SubCategory.objects.order_by("id") 
        return context


@method_decorator(login_required(login_url="signin"),name="dispatch")
class UpdateCategoryView(SuccessMessageMixin,UpdateView):
    model = Category
    template_name = "pages/create_category.html"
    # fields = "__all__"
    form_class = CategoryForm
    success_url = reverse_lazy("show_cat_subcat")
    success_message = "New Category Has Been Added Successfully"
     
@method_decorator(login_required(login_url="signin"),name="dispatch")
class UpdateSubCategoryView(SuccessMessageMixin,UpdateView):
    model = SubCategory
    template_name = "pages/create_subcategory.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("show_cat_subcat")
    success_message = "Sub Category Has Been Updated Successfully"
    
    
@method_decorator(login_required(login_url="signin"),name="dispatch")
class CreateProductView(SuccessMessageMixin,CreateView):
    model = Products
    template_name = "pages/create_products.html"
    form_class = ProductForm
    success_url = reverse_lazy("show_products")
    success_message = "New Product Has Been Added Successfully"

@method_decorator(login_required(login_url="signin"),name="dispatch")
class UpdateProductView(SuccessMessageMixin,UpdateView):
    model = Products
    template_name = "pages/create_products.html"
    form_class = ProductForm
    success_url = reverse_lazy("show_products")
    success_message = "Product Has Been Updated Successfully"

    
@method_decorator(login_required(login_url="signin"),name="dispatch")
class ListProductView(ListView):
    model = Products
    template_name = "pages/show_products.html"
    # context_object_name = "product_list"
    ordering = ["-date_added"]
    paginate_by = 10
    paginate_orphans = 4
    
    def get_context_data(self, **kwargs):
        try:
            return super(ListProductView,self).get_context_data(**kwargs)
        except Http404:
            self.kwargs["page"]=1
            return super(ListProductView,self).get_context_data(**kwargs)
    


def list_products_view(request):
    products =  Products.objects.all().order_by("id")
    template_name = "pages/show_products_from_fun.html"
    paginator = Paginator(products,5,orphans=2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,template_name,{"page_obj":page_obj})
    

@method_decorator(login_required(login_url="signin"),name="dispatch")
class DetailProductView(TemplateView):
    # model = Products
    template_name = "pages/each_product_detail.html"
    # context_object_name = "product_detail"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"data_exists":False}
        if Products.objects.filter(id=self.kwargs["pk"]).exists():
            context["data_exists"] = True
            context["product_detail"] = Products.objects.get(id=self.kwargs["pk"])
        else:
            messages.success(self.request,"Product Not Found")
        return context
    
    


def search_products(request,id=0):
    template_name = "pages/search_products.html"
    context = {"found":False,"method":True}
    if request.method=="GET":
        context["method"]=False
        return render(request,template_name)
 
    if request.method == "POST":
        if request.POST.get("searched") == "":
            context["message"] = "Your Search Was Empty"
        else:
            id = int(request.POST.get("searched"))
            if Products.objects.filter(id=id).exists():
                product_detail = Products.objects.get(id=id)
                context["product_detail"] = product_detail
                context["found"] = True
            else:
                context["message"] = "Please Enter Correct ID. The Id You have entered Not been Found! Try Again"
                
        return render(request,template_name,context)
    else:
        return render(request,template_name)



@method_decorator(login_required(login_url="signin"),name="dispatch")
class SoldFormView(SuccessMessageMixin,FormView):
    template_name = "pages/sold_items.html"
    form_class = SoldProductsFrom
    success_url =  reverse_lazy("dashboard")
    success_message = "Successfully  Added Sold Product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Products.objects.get(id=self.kwargs['id'])
        return context
    
    
    def form_valid(self,form):
        product_obj = Products.objects.get(id=self.kwargs['id'])
        if product_obj.product_amount >= form.cleaned_data["product_amount_sold"]:
            product_obj.sold(form.cleaned_data["product_amount_sold"])
            product_obj.save()
            product_sold_obj = SoldProducts(
                product_sold=product_obj,
                product_selling_price=form.cleaned_data["product_selling_price"],
                product_amount_sold = form.cleaned_data["product_amount_sold"],
                added_date = form.cleaned_data["added_date"],
                )
            product_sold_obj.save()
            message = "हजुरको  ईन्ट्रि हामिलाई प्राप्त भयो । धन्यवाद ! "
            messages.success(self.request,message)
            return redirect("search_products",0)
        else:
            mydata = form.cleaned_data["product_amount_sold"]
            print("Hello World")
            message = "हामी सङ्ग जम्मा ",product_obj.product_amount, " ओटा सामान छ  र  हजुर ले ",mydata,"ओटा सामान बेचे भनेर पठाउनु भयको छ । कृपया पुनः चेक गरेर पठाउनु होस् । धन्यबाद ! "
            messages.success(self.request,message)
            return redirect("sold_form",self.kwargs['id'])
        return super().form_valid(form)


@method_decorator(login_required(login_url="signin"),name="dispatch")
class SoldProductsView(ListView):
    model = SoldProducts
    # context_object_name = "products_sold_list"
    template_name = "pages/sold_products_lists.html"
    paginate_by = 8
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_sold_list"] = SoldProducts.objects.order_by("-created_on") 
        return context
    
    def form_valid(self,form):
        id = self.kwargs["date"]
    
    
def view_sold_products(request,date=0):
    template_name = "pages/sold_products_lists.html"
    context = {"products_sold_list":None,"product_found":True,"is_paginated":False,"grand_total":False}
    if request.method =="GET":
        products_sold_list = SoldProducts.objects.all()
        # context["products_sold_list"] = products_sold_list
        paginator = Paginator(products_sold_list, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["is_paginated"] = True
        
    elif request.method == "POST":
        date = request.POST.get("date")
        if SoldProducts.objects.filter(added_date=date).exists():
            filtered_sold_objects = SoldProducts.objects.filter(added_date=date).order_by("-created_on")
            context["page_obj"] = filtered_sold_objects
            context["grand_total"] = True
            total_sold_on_day = 0.0
            total_profit_on_day = 0.0
            for item in filtered_sold_objects:
                total_sold_on_day = total_sold_on_day + item.total_on_each_item()
                total_profit_on_day = total_profit_on_day + item.total_profit_or_loss()
            context["total_sold"] = total_sold_on_day
            context["profit"] = False
            if total_profit_on_day > 0: 
                context["profit"] = True
            context["total_profit"] = total_profit_on_day
            
        else:
            context["product_found"] = False
            messages.success(request, f"No Any Items Were Sold on {date} please try again")
    return render(request,template_name,context)
        
        
        
    


        