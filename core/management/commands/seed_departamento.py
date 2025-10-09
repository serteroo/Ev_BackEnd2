# core/management/commands/seed_departamentos.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import departamento

class Command(BaseCommand):
    help = "Siembra datos iniciales para departamentos"

    def handle(self, *args, **options):
        with transaction.atomic():
            departamentos_data = [
                {
                    "nombre": "Recursos Humanos",
                    "description": "Gestión de personal, nóminas y desarrollo"
                },
                {
                    "nombre": "Finanzas",
                    "description": "Administración financiera y contable"
                },
                {
                    "nombre": "Tecnología de la Información",
                    "description": "Sistemas, infraestructura TI y desarrollo"
                },
                {
                    "nombre": "Operaciones",
                    "description": "Gestión operativa y logística"
                },
                {
                    "nombre": "Ventas y Marketing",
                    "description": "Área comercial y estrategias de mercado"
                },
                {
                    "nombre": "Administración",
                    "description": "Gestión administrativa general"
                },
                {
                    "nombre": "Legal y Cumplimiento",
                    "description": "Asesoría legal y cumplimiento normativo"
                },
                {
                    "nombre": "Desarrollo de Producto",
                    "description": "Investigación y desarrollo de productos"
                },
                {
                    "nombre": "Atención al Cliente",
                    "description": "Soporte y servicio al cliente"
                },
                {
                    "nombre": "Calidad y Procesos",
                    "description": "Control de calidad y mejora de procesos"
                },
                {
                    "nombre": "Compras y Proveedores",
                    "description": "Gestión de compras y relaciones con proveedores"
                },
                {
                    "nombre": "Mantenimiento",
                    "description": "Mantenimiento de instalaciones y equipos"
                },
                {
                    "nombre": "Seguridad y Salud",
                    "description": "Prevención de riesgos y salud laboral"
                },
                {
                    "nombre": "Capacitación",
                    "description": "Desarrollo y formación del personal"
                },
                {
                    "nombre": "Auditoría Interna",
                    "description": "Auditoría y control interno"
                }
            ]

            for dept_data in departamentos_data:
                # Buscar por nombre (campo único)
                obj, created = departamento.objects.get_or_create(
                    nombre=dept_data["nombre"],
                    defaults={
                        "description": dept_data["description"],
                        "status": "ACTIVE"  # Heredado de BaseModel
                    }
                )
                
                if created:
                    self.stdout.write(f"Departamento creado: {dept_data['nombre']}")
                else:
                    # Actualizar si ya existe pero los datos cambiaron
                    obj.description = dept_data["description"]
                    obj.status = "ACTIVE"
                    obj.save()
                    self.stdout.write(f"Departamento actualizado: {dept_data['nombre']}")

        self.stdout.write(self.style.SUCCESS(f"Se sembraron {len(departamentos_data)} departamentos exitosamente"))