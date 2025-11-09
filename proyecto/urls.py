# proyecto/urls.py
from django.contrib import admin
from django.urls import path
from core import views as v

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas
    path('', v.login_page, name='login_page'),
    path('dashboard/', v.dashboard_empleado, name='dash_empleado'),
    path('dashboard-admin/', v.dashboard_admin, name='dash_admin'),

    # Subpáginas empleado
    path('dashboard/horarios/', v.horario_jornada_page, name='horarios'),
    path('dashboard/liquidaciones/', v.liquidacion_page, name='liquidaciones'),
    path('dashboard/contrato/', v.contrato_empleado_page, name='contrato_empleado'),

    # Subpáginas admin
    path('dashboard-admin/horarios/', v.horario_admin_page, name='horarios_admin'),
    path('dashboard-admin/liquidaciones/', v.liquidaciones_admin_page, name='liquidaciones_admin'),
    path('dashboard-admin/contratos/', v.contratos_admin_page, name='contratos_admin'),
    path('dashboard-admin/contrato/', v.contrato_admin_page, name='contrato_admin'),

    # API
    path('api/login/', v.login_json, name='login_json'),
    path('api/logout/', v.logout_view, name='logout'),
    path('api/me/', v.me, name='me'),
]
