from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    PasswordResetCustomView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('',views.index, name="index"),
    path('index_ventas/', views.index_ventas, name="index_ventas"),
    path('inicio/',views.index, name="inicio"),
    path('registro/',views.registrer_page, name="register"),
    path('login/',views.login_page, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('search', views.search, name="search"),
    path('password_reset/', PasswordResetCustomView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]