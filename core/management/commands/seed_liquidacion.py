# core/management/commands/seed_liquidaciones.py
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta
from decimal import Decimal
from core.models import liquidacion, contrato

class Command(BaseCommand):
    help = "Siembra datos iniciales para liquidaciones de sueldo"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Primero necesitamos obtener contratos existentes
            contratos_activos = contrato.objects.filter(status="ACTIVE", fecha_fin__isnull=True)
            
            if not contratos_activos.exists():
                self.stdout.write(self.style.ERROR("No hay contratos activos existentes. Ejecuta seed_contratos primero."))
                return

            liquidaciones_data = []
            
            # Generar liquidaciones para los últimos 6 meses para cada contrato activo
            for contrato_obj in contratos_activos:
                empleado_nombre = contrato_obj.empleado.user.get_full_name()
                cargo_nombre = contrato_obj.cargo.nombre
                
                # Valores base según el cargo (simulación)
                if "Gerente" in cargo_nombre:
                    base_imponible = Decimal('2500000')
                elif "Jefe" in cargo_nombre or "Senior" in cargo_nombre:
                    base_imponible = Decimal('1800000')
                elif "Analista" in cargo_nombre:
                    base_imponible = Decimal('1200000')
                elif "Desarrollador" in cargo_nombre:
                    base_imponible = Decimal('1500000')
                elif "Contador" in cargo_nombre:
                    base_imponible = Decimal('1400000')
                elif "Ejecutivo" in cargo_nombre:
                    base_imponible = Decimal('900000')
                elif "Asistente" in cargo_nombre:
                    base_imponible = Decimal('700000')
                elif "Administrador" in cargo_nombre:
                    base_imponible = Decimal('1100000')
                else:
                    base_imponible = Decimal('800000')
                
                # Generar 6 liquidaciones mensuales (últimos 6 meses)
                for i in range(6):
                    periodo = date.today().replace(day=1) - timedelta(days=30*i)
                    if periodo < contrato_obj.fecha_inicio:
                        continue  # Saltar periodos antes del inicio del contrato
                    
                    # Calcular valores (simulación realista)
                    no_imponible = base_imponible * Decimal('0.1')  # 10% no imponible
                    tributable = base_imponible - no_imponible
                    descuentos = tributable * Decimal('0.17')  # Aprox. 17% descuentos (AFP, salud, etc.)
                    anticipo = Decimal('150000') if i == 0 else Decimal('0')  # Anticipo solo en primera liquidación
                    liquido = base_imponible - descuentos - anticipo
                    
                    # Fechas relacionadas
                    fecha_pago = periodo + timedelta(days=5)  # Pago alrededor del día 5
                    devengado = periodo  # Mismo que periodo
                    cierre = periodo + timedelta(days=30)  # Cierre del periodo
                    
                    # Estado según la fecha
                    if fecha_pago > date.today():
                        estado = "PENDIENTE"
                    else:
                        estado = "PAGADO"
                    
                    liquidaciones_data.append({
                        "contrato": contrato_obj,
                        "empleado_nombre": empleado_nombre,
                        "periodo": periodo,
                        "fecha_pago": fecha_pago,
                        "imponible": base_imponible,
                        "no_imponible": no_imponible,
                        "tributable": tributable,
                        "descuentos": descuentos,
                        "anticipo": anticipo,
                        "liquido": liquido,
                        "devengado": devengado,
                        "cierre": cierre,
                        "estado": estado
                    })

            liquidaciones_creadas = 0

            for liq_data in liquidaciones_data:
                try:
                    # Buscar por contrato y periodo (combinación única)
                    liquidacion_obj, created = liquidacion.objects.get_or_create(
                        contrato=liq_data["contrato"],
                        periodo=liq_data["periodo"],
                        defaults={
                            "fecha_pago": liq_data["fecha_pago"],
                            "imponible": liq_data["imponible"],
                            "no_imponible": liq_data["no_imponible"],
                            "tributable": liq_data["tributable"],
                            "descuentos": liq_data["descuentos"],
                            "anticipo": liq_data["anticipo"],
                            "liquido": liq_data["liquido"],
                            "devengado": liq_data["devengado"],
                            "cierre": liq_data["cierre"],
                            "estado": liq_data["estado"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        liquidaciones_creadas += 1
                        self.stdout.write(f"Liquidación creada: {liq_data['empleado_nombre']} - {liq_data['periodo'].strftime('%Y-%m')} - ${liq_data['liquido']:,.0f}")
                    else:
                        # Actualizar liquidación existente
                        liquidacion_obj.fecha_pago = liq_data["fecha_pago"]
                        liquidacion_obj.imponible = liq_data["imponible"]
                        liquidacion_obj.no_imponible = liq_data["no_imponible"]
                        liquidacion_obj.tributable = liq_data["tributable"]
                        liquidacion_obj.descuentos = liq_data["descuentos"]
                        liquidacion_obj.anticipo = liq_data["anticipo"]
                        liquidacion_obj.liquido = liq_data["liquido"]
                        liquidacion_obj.devengado = liq_data["devengado"]
                        liquidacion_obj.cierre = liq_data["cierre"]
                        liquidacion_obj.estado = liq_data["estado"]
                        liquidacion_obj.status = "ACTIVE"
                        liquidacion_obj.save()
                        self.stdout.write(f"Liquidación actualizada: {liq_data['empleado_nombre']} - {liq_data['periodo'].strftime('%Y-%m')}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando liquidación para {liq_data['empleado_nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(liquidaciones_data)} liquidaciones, {liquidaciones_creadas} nuevas creadas"))