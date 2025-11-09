from django.contrib import admin
from .models import (
    cargo, departamento, direccion, forma_pago, jornada, roles, turno,
    empleado, cuenta_bancaria, contrato, liquidacion, pago, turno_has_jornada, ZonaTrabajo
)
from .forms import PagoForm
from core.scoping import _get_employee_for_user, _apply_scope




# ---------- Helpers ----------
BASE_READONLY = ("created_at", "updated_at")
BASE_LIST = ("status",) + BASE_READONLY

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = BASE_READONLY
    list_filter = ("status",)
    list_per_page = 25

# ---------- Inlines ----------
class CuentaBancariaInline(admin.TabularInline):
    model = cuenta_bancaria
    extra = 0
    fields = ("banco", "tipo_cuenta", "numero_cuenta", "correo", "status")
    readonly_fields = BASE_READONLY

class PagoInline(admin.TabularInline):
    model = pago
    form = PagoForm
    extra = 0
    fields = ("fecha_pago", "monto", "forma_pago", "comprobante", "estado", "status")
    readonly_fields = BASE_READONLY

#---------acciones---------------
@admin.action(description="Marcar seleccionados como activos")
def make_active(modeladmin, request, queryset):
    queryset.update(status="ACTIVE")

@admin.action(description="Marcar seleccionados como inactivos")
def make_inactive(modeladmin, request, queryset):
    queryset.update(status="INACTIVE")

#---Scoping---#

class ScopedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        empleado = _get_employee_for_user(request.user)
        return _apply_scope(qs, empleado)



# ---------- Catálogos ----------
@admin.register(direccion)
class DireccionAdmin(BaseAdmin):
    list_display = ("id", "calle", "numero", "comuna", "region", "codigo_postal") + BASE_LIST
    search_fields = ("calle", "comuna", "region", "codigo_postal")
    list_filter = ("region", "comuna", "status")
    list_ordering = ("calle",)

@admin.register(roles)
class RolesAdmin(BaseAdmin):
    list_display = ("id", "nombre", "description") + BASE_LIST
    search_fields = ("nombre",)
    list_filter = ("status",)
    list_ordering = ("nombre",)

@admin.register(departamento)
class DepartamentoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "description") + BASE_LIST
    search_fields = ("nombre",)
    list_filter = ("status",)
    list_ordering = ("nombre",)

@admin.register(cargo)
class CargoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "description") + BASE_LIST
    search_fields = ("nombre",)
    list_filter = ("status",)
    list_ordering = ("nombre",)

@admin.register(forma_pago)
class FormaPagoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "description") + BASE_LIST
    search_fields = ("nombre",)
    list_filter = ("status",)
    list_ordering = ("nombre",)

@admin.register(jornada)
class JornadaAdmin(BaseAdmin):
    list_display = ("id", "nombre", "horas_semanales") + BASE_LIST
    search_fields = ("nombre",)
    list_filter = ("status",)
    list_ordering = ("nombre",)

@admin.register(turno)
class TurnoAdmin(BaseAdmin):
    list_display = ("id", "hora_entrada", "hora_salida") + BASE_LIST
    search_fields = ("hora_entrada", "hora_salida")
    list_filter = ("status",)
    list_ordering = ("hora_entrada",)
   
    

# ---------- Relaciones ----------
@admin.register(turno_has_jornada)
class TurnoHasJornadaAdmin(BaseAdmin):
    list_display = ("id", "turno", "jornada") + BASE_LIST
    list_select_related = ("turno", "jornada")
    search_fields = ("turno__id", "jornada__nombre")
    list_filter = ("turno__hora_entrada", "jornada__nombre", "status")
    list_ordering = ("turno__hora_entrada", "jornada__nombre")

# ---------- Nucleares ----------
@admin.register(empleado)
class EmpleadoAdmin(BaseAdmin):
    list_display = ("id", "run", "user", "fono", "nacionalidad") + BASE_LIST
    search_fields = ("run", "user__username", "user__email")
    list_select_related = ("user",)
    actions = [make_active, make_inactive]
    list_filter = ("nacionalidad", "status")
    list_ordering = ("run",)
    inlines = [CuentaBancariaInline]

@admin.register(cuenta_bancaria)
class CuentaBancariaAdmin(ScopedAdmin, BaseAdmin):
    list_display = ("id", "empleado", "banco", "tipo_cuenta", "numero_cuenta", "correo") + BASE_LIST
    list_select_related = ("empleado",)
    search_fields = ("empleado__run", "empleado__user__username", "banco", "numero_cuenta")
    list_filter = ("banco", "tipo_cuenta", "status")
    list_ordering = ("empleado__run", "banco")

@admin.register(contrato)
class ContratoAdmin(ScopedAdmin, BaseAdmin):
    list_display = (
        "id", "empleado", "departamento", "cargo",
        "fecha_inicio", "fecha_fin", "turno_has_jornada"
    ) + BASE_LIST
    list_select_related = ("empleado", "departamento", "cargo", "turno_has_jornada")
    search_fields = (
        "empleado__run", "empleado__user__username",
        "departamento__nombre", "cargo__nombre",
    )
    autocomplete_fields = ("empleado", "departamento", "cargo", "turno_has_jornada")
    list_filter = ("departamento", "cargo", "status")
    list_ordering = ("empleado__run", "fecha_inicio")

@admin.register(liquidacion)
class LiquidacionAdmin(ScopedAdmin, BaseAdmin):
    list_display = (
        "id", "contrato", "periodo", "fecha_pago",
        "imponible", "no_imponible", "tributable",
        "descuentos", "anticipo", "liquido", "estado"
    ) + BASE_LIST
    list_select_related = ("contrato",)
    search_fields = ("contrato__empleado__run", "est_contrato__empleado__user__username")
    list_filter = ("estado", "status")
    list_ordering = ("-periodo", "contrato__empleado__run")

@admin.register(pago)
class PagoAdmin(ScopedAdmin, BaseAdmin):
    list_display = ("id", "liquidacion", "fecha_pago", "monto", "forma_pago", "estado") + BASE_LIST
    list_select_related = ("liquidacion", "forma_pago")
    search_fields = ("liquidacion__contrato__empleado__run", "liquidacion__contrato__empleado__user__username")
    list_filter = ("estado", "forma_pago", "status")
    list_ordering = ("-fecha_pago", "liquidacion__contrato__empleado__run")
    actions = [make_active, make_inactive]
    form = PagoForm


@admin.register(ZonaTrabajo)
class ZonaTrabajoAdmin(ScopedAdmin, BaseAdmin):
    list_display = ("nombre", "area", "ubicacion", "supervisor")
    search_fields = ("nombre", "area", "ubicacion", "supervisor")



