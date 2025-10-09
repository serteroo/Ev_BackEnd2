# core/management/commands/seed_cuentas_bancarias.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import cuenta_bancaria, empleado

class Command(BaseCommand):
    help = "Siembra datos iniciales para cuentas bancarias"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Primero necesitamos obtener algunos empleados existentes
            empleados = empleado.objects.filter(status="ACTIVE")[:10]
            
            if not empleados.exists():
                self.stdout.write(self.style.ERROR("No hay empleados existentes. Ejecuta seed_empleados primero."))
                return

            cuentas_data = [
                {
                    "banco": "Banco de Chile",
                    "tipo_cuenta": "Cuenta Corriente",
                    "numero_cuenta": 1234567890123456,
                    "correo": "admin.rh@empresa.com"
                },
                {
                    "banco": "Banco Estado",
                    "tipo_cuenta": "Cuenta Vista",
                    "numero_cuenta": 2345678901234567,
                    "correo": "maria.contreras@empresa.com"
                },
                {
                    "banco": "Scotiabank",
                    "tipo_cuenta": "Cuenta Corriente",
                    "numero_cuenta": 3456789012345678,
                    "correo": "carlos.munoz@empresa.com"
                },
                {
                    "banco": "BCI",
                    "tipo_cuenta": "Cuenta Ahorro",
                    "numero_cuenta": 4567890123456789,
                    "correo": "juan.perez@empresa.com"
                },
                {
                    "banco": "Santander",
                    "tipo_cuenta": "Cuenta Corriente",
                    "numero_cuenta": 5678901234567890,
                    "correo": "laura.torres@empresa.com"
                },
                {
                    "banco": "Itaú",
                    "tipo_cuenta": "Cuenta Vista",
                    "numero_cuenta": 6789012345678901,
                    "correo": "roberto.sanchez@empresa.com"
                },
                {
                    "banco": "Banco Falabella",
                    "tipo_cuenta": "Cuenta Corriente",
                    "numero_cuenta": 7890123456789012,
                    "correo": "patricia.mendoza@empresa.com"
                },
                {
                    "banco": "Banco BICE",
                    "tipo_cuenta": "Cuenta Ahorro",
                    "numero_cuenta": 8901234567890123,
                    "correo": "miguel.herrera@empresa.com"
                },
                {
                    "banco": "HSBC",
                    "tipo_cuenta": "Cuenta Corriente",
                    "numero_cuenta": 9012345678901234,
                    "correo": "daniela.rios@empresa.com"
                },
                {
                    "banco": "Banco Security",
                    "tipo_cuenta": "Cuenta Vista",
                    "numero_cuenta": 1122334455667788,
                    "correo": "fernando.guzman@empresa.com"
                },
                # Cuenta adicional para el primer empleado
                {
                    "banco": "Banco Ripley",
                    "tipo_cuenta": "Cuenta Ahorro",
                    "numero_cuenta": 2233445566778899,
                    "correo": "admin.rh@empresa.com"
                }
            ]

            cuentas_creadas = 0

            for i, cuenta_data in enumerate(cuentas_data):
                try:
                    # Asignar empleado en orden cíclico
                    empleado_asignado = empleados[i % len(empleados)]
                    
                    # Buscar por número de cuenta (debería ser único)
                    cuenta_obj, created = cuenta_bancaria.objects.get_or_create(
                        numero_cuenta=cuenta_data["numero_cuenta"],
                        defaults={
                            "empleado": empleado_asignado,
                            "banco": cuenta_data["banco"],
                            "tipo_cuenta": cuenta_data["tipo_cuenta"],
                            "correo": cuenta_data["correo"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        cuentas_creadas += 1
                        self.stdout.write(f"Cuenta bancaria creada: {cuenta_data['banco']} - {cuenta_data['numero_cuenta']} para {empleado_asignado.user.get_full_name()}")
                    else:
                        # Actualizar cuenta existente
                        cuenta_obj.empleado = empleado_asignado
                        cuenta_obj.banco = cuenta_data["banco"]
                        cuenta_obj.tipo_cuenta = cuenta_data["tipo_cuenta"]
                        cuenta_obj.correo = cuenta_data["correo"]
                        cuenta_obj.status = "ACTIVE"
                        cuenta_obj.save()
                        self.stdout.write(f"Cuenta bancaria actualizada: {cuenta_data['banco']} - {cuenta_data['numero_cuenta']}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando cuenta bancaria: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(cuentas_data)} cuentas bancarias, {cuentas_creadas} nuevas creadas"))