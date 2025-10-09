# core/management/commands/seed_pagos.py
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta
from decimal import Decimal
from core.models import pago, liquidacion, forma_pago

class Command(BaseCommand):
    help = "Siembra datos iniciales para pagos"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Primero necesitamos obtener liquidaciones y formas de pago existentes
            liquidaciones_pagadas = liquidacion.objects.filter(
                status="ACTIVE", 
                estado="PAGADO"
            )[:20]  # Limitar a 20 liquidaciones para no crear demasiados pagos
            
            formas_pago_activas = forma_pago.objects.filter(status="ACTIVE")
            
            if not liquidaciones_pagadas.exists():
                self.stdout.write(self.style.ERROR("No hay liquidaciones pagadas existentes. Ejecuta seed_liquidaciones primero."))
                return
                
            if not formas_pago_activas.exists():
                self.stdout.write(self.style.ERROR("No hay formas de pago existentes. Ejecuta seed_formas_pago primero."))
                return

            pagos_data = []
            
            # Generar pagos para las liquidaciones pagadas
            for i, liquidacion_obj in enumerate(liquidaciones_pagadas):
                empleado_nombre = liquidacion_obj.contrato.empleado.user.get_full_name()
                monto_liquido = liquidacion_obj.liquido
                periodo = liquidacion_obj.periodo.strftime('%Y-%m')
                
                # Asignar forma de pago según índice (rotar entre las disponibles)
                forma_pago_obj = formas_pago_activas[i % formas_pago_activas.count()]
                
                # Generar datos del pago
                fecha_pago = liquidacion_obj.fecha_pago or (liquidacion_obj.periodo + timedelta(days=5))
                
                # Para algunos pagos, crear múltiples pagos (parciales)
                if i % 5 == 0:  # Cada 5to pago es parcial
                    # Primer pago parcial (70%)
                    pagos_data.append({
                        "liquidacion": liquidacion_obj,
                        "forma_pago": forma_pago_obj,
                        "empleado_nombre": empleado_nombre,
                        "periodo": periodo,
                        "fecha_pago": fecha_pago - timedelta(days=2),
                        "monto": monto_liquido * Decimal('0.7'),
                        "comprobante": f"COMP-{periodo}-{empleado_nombre.split()[0]}-1",
                        "estado": "COMPLETADO"
                    })
                    # Segundo pago parcial (30%)
                    pagos_data.append({
                        "liquidacion": liquidacion_obj,
                        "forma_pago": formas_pago_activas[(i + 1) % formas_pago_activas.count()],
                        "empleado_nombre": empleado_nombre,
                        "periodo": periodo,
                        "fecha_pago": fecha_pago,
                        "monto": monto_liquido * Decimal('0.3'),
                        "comprobante": f"COMP-{periodo}-{empleado_nombre.split()[0]}-2",
                        "estado": "COMPLETADO"
                    })
                else:
                    # Pago único
                    estado = "COMPLETADO" if fecha_pago < date.today() else "PENDIENTE"
                    
                    pagos_data.append({
                        "liquidacion": liquidacion_obj,
                        "forma_pago": forma_pago_obj,
                        "empleado_nombre": empleado_nombre,
                        "periodo": periodo,
                        "fecha_pago": fecha_pago,
                        "monto": monto_liquido,
                        "comprobante": f"COMP-{periodo}-{empleado_nombre.split()[0]}",
                        "estado": estado
                    })

            pagos_creados = 0

            for pago_data in pagos_data:
                try:
                    # Buscar por liquidación y comprobante (podría ser único)
                    pago_obj, created = pago.objects.get_or_create(
                        liquidacion=pago_data["liquidacion"],
                        comprobante=pago_data["comprobante"],
                        defaults={
                            "fecha_pago": pago_data["fecha_pago"],
                            "monto": pago_data["monto"],
                            "estado": pago_data["estado"],
                            "forma_pago": pago_data["forma_pago"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        pagos_creados += 1
                        self.stdout.write(f"Pago creado: {pago_data['empleado_nombre']} - {pago_data['periodo']} - ${pago_data['monto']:,.0f} - {pago_data['forma_pago'].nombre}")
                    else:
                        # Actualizar pago existente
                        pago_obj.fecha_pago = pago_data["fecha_pago"]
                        pago_obj.monto = pago_data["monto"]
                        pago_obj.estado = pago_data["estado"]
                        pago_obj.forma_pago = pago_data["forma_pago"]
                        pago_obj.status = "ACTIVE"
                        pago_obj.save()
                        self.stdout.write(f"Pago actualizado: {pago_data['empleado_nombre']} - {pago_data['periodo']}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando pago para {pago_data['empleado_nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(pagos_data)} pagos, {pagos_creados} nuevos creados"))