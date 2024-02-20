from django.urls import path
from . import views

urlpatterns = [
    path('calendario', views.calendario, name="calendario"),
    path('all_events', views.all_events, name="all_events"),
    path('add_event', views.add_event, name="add_event"),
    path('remove', views.remove, name='remove'),
]