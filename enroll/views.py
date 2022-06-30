from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import forms as my_form
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

@method_decorator(login_required(login_url="signin"),name="dispatch")
class DashboardView(TemplateView):
    template_name = "pages/dashboard.html"
    
@method_decorator(login_required(login_url="signin"),name="dispatch")
class TableView(TemplateView):
    template_name = "pages/tables.html"
 
@method_decorator(login_required(login_url="signin"),name="dispatch")   
class BillingView(TemplateView):
    template_name = "pages/billing.html"

@method_decorator(login_required(login_url="signin"),name="dispatch")   
class NotificationView(TemplateView):
    template_name = "pages/notifications.html"

@method_decorator(login_required(login_url="signin"),name="dispatch")
class ProfileView(TemplateView):
    template_name = "pages/profile.html"

class SignupView(TemplateView):
    template_name = "pages/sign-up.html"


class SigninView(auth_views.LoginView):
    template_name = "pages/sign-in.html"
    authentication_form = my_form.SinginForm
    
    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request,*args,**kwargs)


@method_decorator(login_required(login_url="signin"),name="dispatch")
class ChangePassword(SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name = "pages/changepassword.html"
    success_message = "Your Password Was Successfully Changed"
    success_url = reverse_lazy("profile")
    form_class = my_form.ChangePasswordForm


class ResetPasswordView(SuccessMessageMixin,auth_views.PasswordResetView):
    form_class = my_form.ResetPasswordForm
    template_name = "pages/resetpassword.html"
    success_url = reverse_lazy("signin")
    success_message = "A reset link has been successfully sent to your Email. If your didnot recieve it please try with "\
        "Valid Email"
    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request,*args,**kwargs)

class SetPasswordView(SuccessMessageMixin,auth_views.PasswordResetConfirmView):
    form_class= my_form.SetPasswordForm
    template_name = "pages/setpassword.html"
    success_url = reverse_lazy("signin")
    success_message = "Your Password Has been Successfully Reset. Please try Signin with your new password.Thank You!"
    
    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request,*args,**kwargs)    
    