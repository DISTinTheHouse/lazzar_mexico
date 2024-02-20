from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('listar_tickets/', views.listar_tickets, name='listar_tickets'),
    path('ticket/<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('ticket/<int:ticket_id>/agregar-respuesta/', views.agregar_respuesta, name='agregar_respuesta'),
    path('crear-ticket/', views.crear_ticket, name='crear_ticket'),
    path('asignar-ticket/<int:ticket_id>/', views.asignar_ticket, name='asignar_ticket'),
    path('cambia-status/<int:ticket_id>/', views.cambia_status, name='cambia_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)