# core/management/commands/seed_formas_pago.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import forma_pago

class Command(BaseCommand):
    help = "Siembra datos iniciales para formas de pago"

    def handle(self, *args, **options):
        with transaction.atomic():
            formas_pago_data = [
                {
                    "nombre": "Transferencia Bancaria",
                    "description": "Pago mediante transferencia electrónica"
                },
                {
                    "nombre": "Depósito Directo",
                    "description": "Depósito automático en cuenta bancaria"
                },
                {
                    "nombre": "Cheque",
                    "description": "Pago mediante cheque nominativo"
                },
                {
                    "nombre": "Efectivo",
                    "description": "Pago en efectivo en caja"
                },
                {
                    "nombre": "Vale Vista",
                    "description": "Pago mediante vale vista bancario"
                },
                {
                    "nombre": "Pago Mixto",
                    "description": "Combinación de diferentes formas de pago"
                },
                {
                    "nombre": "Pago Electrónico",
                    "description": "Pago mediante plataforma electrónica"
                },
                {
                    "nombre": "Retención Bancaria",
                    "description": "Retención automática por entidad bancaria"
                },
                {
                    "nombre": "Orden de Pago",
                    "description": "Pago mediante orden administrativa"
                },
                {
                    "nombre": "Compensación",
                    "description": "Pago mediante compensación de deudas"
                },
                {
                    "nombre": "Pago Diferido",
                    "description": "Pago programado para fecha futura"
                },
                {
                    "nombre": "Pago Parcial",
                    "description": "Pago fraccionado en varias cuotas"
                },
                {
                    "nombre": "Pago en Especies",
                    "description": "Pago mediante bienes o servicios"
                },
                {
                    "nombre": "Pago Internacional",
                    "description": "Transferencia internacional SWIFT"
                },
                {
                    "nombre": "Pago Móvil",
                    "description": "Pago mediante aplicación móvil"
                },
                {
                    "nombre": "Débito Automático",
                    "description": "Débito automático desde cuenta"
                },
                {
                    "nombre": "Crédito en Cuenta",
                    "description": "Abono directo en cuenta corriente"
                },
                {
                    "nombre": "Pago con Retención",
                    "description": "Pago con retención de impuestos"
                },
                {
                    "nombre": "Pago a Terceros",
                    "description": "Pago dirigido a tercera persona"
                },
                {
                    "nombre": "Pago por Caja Chica",
                    "description": "Pago mediante fondo de caja chica"
                }
            ]

            formas_creadas = 0

            for forma_data in formas_pago_data:
                try:
                    # Buscar por nombre (campo único)
                    forma_obj, created = forma_pago.objects.get_or_create(
                        nombre=forma_data["nombre"],
                        defaults={
                            "description": forma_data["description"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        formas_creadas += 1
                        self.stdout.write(f"Forma de pago creada: {forma_data['nombre']}")
                    else:
                        # Actualizar forma de pago existente
                        if forma_obj.description != forma_data["description"]:
                            forma_obj.description = forma_data["description"]
                            forma_obj.save()
                            self.stdout.write(f"Forma de pago actualizada: {forma_data['nombre']}")
                        else:
                            self.stdout.write(f"Forma de pago existente: {forma_data['nombre']}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando forma de pago {forma_data['nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(formas_pago_data)} formas de pago, {formas_creadas} nuevas creadas"))