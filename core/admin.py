from django.contrib import admin
from .models import (
    cargo, departamento, direccion, forma_pago, jornada, roles, turno,
    empleado, cuenta_bancaria, contrato, liquidacion, pago, turno_has_jornada
)

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
    extra = 0
    fields = ("fecha_pago", "monto", "forma_pago", "comprobante", "estado", "status")
    readonly_fields = BASE_READONLY

# ---------- Catálogos ----------
@admin.register(direccion)
class DireccionAdmin(BaseAdmin):
    list_display = ("id", "calle", "numero", "comuna", "region", "codigo_postal") + BASE_LIST
    search_fields = ("calle", "comuna", "region", "codigo_postal")

@admin.register(roles)
class RolesAdmin(BaseAdmin):
    list_display = ("id", "nombre", "descripcion") + BASE_LIST
    search_fields = ("nombre",)

@admin.register(departamento)
class DepartamentoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "descripcion") + BASE_LIST
    search_fields = ("nombre",)

@admin.register(cargo)
class CargoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "descripcion") + BASE_LIST
    search_fields = ("nombre",)

@admin.register(forma_pago)
class FormaPagoAdmin(BaseAdmin):
    list_display = ("id", "nombre", "descripcion") + BASE_LIST
    search_fields = ("nombre",)

@admin.register(jornada)
class JornadaAdmin(BaseAdmin):
    list_display = ("id", "nombre", "horas_semanales") + BASE_LIST
    search_fields = ("nombre",)

@admin.register(turno)
class TurnoAdmin(BaseAdmin):
    list_display = ("id", "hora_entrada", "hora_salida") + BASE_LIST

# ---------- Relaciones ----------
@admin.register(turno_has_jornada)
class TurnoHasJornadaAdmin(BaseAdmin):
    list_display = ("id", "turno", "jornada") + BASE_LIST
    list_select_related = ("turno", "jornada")
    search_fields = ("turno__id", "jornada__nombre")

# ---------- Nucleares ----------
@admin.register(empleado)
class EmpleadoAdmin(BaseAdmin):
    list_display = ("id", "run", "user", "fono", "nacionalidad") + BASE_LIST
    search_fields = ("run", "user__username", "user__email")
    list_select_related = ("user",)
    inlines = [CuentaBancariaInline]

@admin.register(cuenta_bancaria)
class CuentaBancariaAdmin(BaseAdmin):
    list_display = ("id", "empleado", "banco", "tipo_cuenta", "numero_cuenta", "correo") + BASE_LIST
    list_select_related = ("empleado",)
    search_fields = ("empleado__run", "empleado__user__username", "banco", "numero_cuenta")

@admin.register(contrato)
class ContratoAdmin(BaseAdmin):
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

@admin.register(liquidacion)
class LiquidacionAdmin(BaseAdmin):
    list_display = (
        "id", "contrato", "periodo", "fecha_pago",
        "imponible", "no_imponible", "tributable",
        "descuentos", "anticipo", "liquido", "estado"
    ) + BASE_LIST
    list_select_related = ("contrato",)
    search_fields = ("contrato__empleado__run", "est_contrato__empleado__user__username")