# core/management/commands/seed_roles.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import roles

class Command(BaseCommand):
    help = "Siembra datos iniciales para roles del sistema"

    def handle(self, *args, **options):
        with transaction.atomic():
            roles_data = [
                {
                    "nombre": "Administrador",
                    "description": "Acceso completo a todas las funcionalidades del sistema"
                },
                {
                    "nombre": "Gerente RH",
                    "description": "Gestión de recursos humanos, contratos y nóminas"
                },
                {
                    "nombre": "Jefe de Departamento",
                    "description": "Supervisión de departamento específico y su personal"
                },
                {
                    "nombre": "Supervisor",
                    "description": "Supervisión de equipos y coordinación operativa"
                },
                {
                    "nombre": "Contador",
                    "description": "Gestión de liquidaciones, pagos y aspectos contables"
                },
                {
                    "nombre": "Analista RH",
                    "description": "Análisis y apoyo en gestión de recursos humanos"
                },
                {
                    "nombre": "Empleado",
                    "description": "Acceso básico para consulta de información personal"
                },
                {
                    "nombre": "Auditor",
                    "description": "Revisión y auditoría de procesos y documentación"
                },
            ]

            for rol_data in roles_data:
                # Buscar por nombre (campo único)
                obj, created = roles.objects.get_or_create(
                    nombre=rol_data["nombre"],
                    defaults={
                        "description": rol_data["description"],
                        "status": "ACTIVE"  # Heredado de BaseModel
                    }
                )
                
                if created:
                    self.stdout.write(f"Rol creado: {rol_data['nombre']}")
                else:
                    # Actualizar si ya existe pero los datos cambiaron
                    obj.description = rol_data["description"]
                    obj.status = "ACTIVE"
                    obj.save()
                    self.stdout.write(f"Rol actualizado: {rol_data['nombre']}")

        self.stdout.write(self.style.SUCCESS(f"Se sembraron {len(roles_data)} roles exitosamente"))