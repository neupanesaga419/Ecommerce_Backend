from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    # path("",DashboardView.as_view(),name="dashboard"),
    path("table/",TableView.as_view(),name="table"),
    path("billing/",BillingView.as_view(),name="billing"),
    path("notification/",NotificationView.as_view(),name="notifications"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("signup/",SignupView.as_view(),name="signup"),
    path("signin/",SigninView.as_view(),name="signin"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("changepassword/",ChangePassword.as_view(),name="changepass"),
    path("forgotpassword/",ResetPasswordView.as_view(),name="resetpassword"),
    path("password_reset_confirm/<uidb64>/<token>/",SetPasswordView.as_view(),name="password_reset_confirm"),
]
