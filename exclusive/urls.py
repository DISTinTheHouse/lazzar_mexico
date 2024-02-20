from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login_intranet/', views.login_page, name='login-exclusive'),
    path('inicio-exclusive/',views.index_exclusive, name="index-exclusive"),
]
