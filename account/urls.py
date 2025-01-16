from django.urls import path,reverse_lazy
from . import views 
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('login/',auth_view.LoginView.as_view(template_name="account/login.html"),name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path("change_password/",auth_view.PasswordChangeView.as_view(success_url=reverse_lazy("change_password_done"),template_name="account/change_password.html"),name="change_password"),
    path("change_password_done/",auth_view.PasswordChangeView.as_view(template_name="account/change_password_done.html"),name="change_password_done")

]