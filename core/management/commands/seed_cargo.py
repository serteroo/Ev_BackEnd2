# core/management/commands/seed_cargos.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import cargo

class Command(BaseCommand):
    help = "Siembra datos iniciales para cargos"

    def handle(self, *args, **options):
        with transaction.atomic():
            cargos_data = [
                {
                    "nombre": "Gerente General",
                    "description": "Dirección general de la organización"
                },
                {
                    "nombre": "Gerente de Recursos Humanos",
                    "description": "Dirección del área de recursos humanos"
                },
                {
                    "nombre": "Gerente Financiero",
                    "description": "Dirección del área financiera y contable"
                },
                {
                    "nombre": "Gerente de TI",
                    "description": "Dirección de tecnología de la información"
                },
                {
                    "nombre": "Gerente de Operaciones",
                    "description": "Dirección del área operativa"
                },
                {
                    "nombre": "Jefe de Departamento",
                    "description": "Supervisión de departamento específico"
                },
                {
                    "nombre": "Supervisor de Área",
                    "description": "Supervisión operativa de área específica"
                },
                {
                    "nombre": "Contador General",
                    "description": "Contabilidad general y estados financieros"
                },
                {
                    "nombre": "Analista Financiero",
                    "description": "Análisis y reportes financieros"
                },
                {
                    "nombre": "Analista de RH",
                    "description": "Análisis y procesos de recursos humanos"
                },
                {
                    "nombre": "Desarrollador Senior",
                    "description": "Desarrollo de software avanzado"
                },
                {
                    "nombre": "Desarrollador Junior",
                    "description": "Desarrollo de software básico"
                },
                {
                    "nombre": "Administrador de Sistemas",
                    "description": "Gestión de infraestructura TI"
                },
                {
                    "nombre": "Ejecutivo de Ventas",
                    "description": "Gestión comercial y ventas"
                },
                {
                    "nombre": "Especialista en Marketing",
                    "description": "Estrategias y campañas de marketing"
                },
                {
                    "nombre": "Asistente Administrativo",
                    "description": "Apoyo administrativo general"
                },
                {
                    "nombre": "Coordinador de Proyectos",
                    "description": "Coordinación y seguimiento de proyectos"
                },
                {
                    "nombre": "Analista de Calidad",
                    "description": "Control y aseguramiento de calidad"
                },
                {
                    "nombre": "Técnico Especializado",
                    "description": "Especialista técnico en área específica"
                },
                {
                    "nombre": "Asistente de RH",
                    "description": "Apoyo en procesos de recursos humanos"
                },
                {
                    "nombre": "Auxiliar Contable",
                    "description": "Apoyo en labores contables"
                },
                {
                    "nombre": "Representante de Servicio",
                    "description": "Atención y servicio al cliente"
                },
                {
                    "nombre": "Operario",
                    "description": "Personal operativo de producción"
                },
                {
                    "nombre": "Practicante",
                    "description": "Practicante o pasante en formación"
                }
            ]

            for cargo_data in cargos_data:
                # Buscar por nombre (campo único)
                obj, created = cargo.objects.get_or_create(
                    nombre=cargo_data["nombre"],
                    defaults={
                        "description": cargo_data["description"],
                        "status": "ACTIVE"  # Heredado de BaseModel
                    }
                )
                
                if created:
                    self.stdout.write(f"Cargo creado: {cargo_data['nombre']}")
                else:
                    # Actualizar si ya existe pero los datos cambiaron
                    obj.description = cargo_data["description"]
                    obj.status = "ACTIVE"
                    obj.save()
                    self.stdout.write(f"Cargo actualizado: {cargo_data['nombre']}")

        self.stdout.write(self.style.SUCCESS(f"Se sembraron {len(cargos_data)} cargos exitosamente"))