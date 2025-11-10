from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core import views as v

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas
    path('', v.login_page, name='login_page'),
    path('dashboard/', v.dashboard_empleado, name='dash_empleado'),
    path('dashboard-admin/', v.dashboard_admin, name='dash_admin'),

    # Empleado
    path('dashboard/horarios/', v.horario_page, name='horarios'),
    path('dashboard/liquidaciones/', v.liquidacion_page, name='liquidaciones'),
    path('dashboard/contrato/', v.contrato_empleado_page, name='contrato_empleado'),

    # Admin
    path('dashboard-admin/horarios/', v.horario_admin_page, name='horarios_admin'),
    path('dashboard-admin/liquidaciones/', v.liquidaciones_admin_page, name='liquidaciones_admin'),
    path('dashboard-admin/contratos/', v.contratos_admin_page, name='contratos_admin'),
    path('dashboard-admin/contratos/nuevo/', v.contrato_create, name='contrato_create'),
    path('dashboard-admin/contratos/<int:pk>/editar/', v.contrato_edit, name='contrato_edit'),
    path('dashboard-admin/contratos/<int:pk>/eliminar/', v.contrato_delete, name='contrato_delete'),
    path('dashboard-admin/crud-cargo/', v.crud_cargo_page, name='crud_cargo'),

    # ✅ NUEVAS RUTAS CRUD HORARIO
    path('dashboard-admin/horarios/jornadas/', v.horario_jornada_list, name='horario_jornada'),
    path('dashboard-admin/horarios/jornadas/crear/', v.horario_jornada_create, name='horario_create'),
    path('dashboard-admin/horarios/jornadas/<int:pk>/editar/', v.horario_jornada_update, name='horario_update'),
    path('dashboard-admin/horarios/jornadas/<int:pk>/eliminar/', v.horario_jornada_delete, name='horario_delete'),

    # API
    path('api/login/', v.login_json, name='login_json'),
    path('api/logout/', v.logout_view, name='logout'),
    path('api/me/', v.me, name='me'),
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else [])
