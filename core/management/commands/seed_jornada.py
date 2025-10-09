# core/management/commands/seed_jornadas.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import jornada

class Command(BaseCommand):
    help = "Siembra datos iniciales para jornadas laborales"

    def handle(self, *args, **options):
        with transaction.atomic():
            jornadas_data = [
                {
                    "nombre": "Jornada Completa",
                    "horas_semanales": 45
                },
                {
                    "nombre": "Jornada Parcial",
                    "horas_semanales": 30
                },
                {
                    "nombre": "Medio Tiempo",
                    "horas_semanales": 20
                },
                {
                    "nombre": "Jornada Reducida",
                    "horas_semanales": 35
                },
                {
                    "nombre": "Jornada Intensiva",
                    "horas_semanales": 40
                },
                {
                    "nombre": "Jornada Especial",
                    "horas_semanales": 25
                },
                {
                    "nombre": "Jornada Estudiantil",
                    "horas_semanales": 15
                },
                {
                    "nombre": "Jornada Ejecutiva",
                    "horas_semanales": 45
                },
                {
                    "nombre": "Jornada Comercial",
                    "horas_semanales": 42
                },
                {
                    "nombre": "Jornada Operativa",
                    "horas_semanales": 48
                },
                {
                    "nombre": "Jornada Administrativa",
                    "horas_semanales": 44
                },
                {
                    "nombre": "Jornada Técnica",
                    "horas_semanales": 45
                },
                {
                    "nombre": "Jornada por Turnos",
                    "horas_semanales": 42
                },
                {
                    "nombre": "Jornada Flexible",
                    "horas_semanales": 35
                },
                {
                    "nombre": "Jornada de Temporada",
                    "horas_semanales": 50
                },
                {
                    "nombre": "Jornada Nocturna",
                    "horas_semanales": 36
                },
                {
                    "nombre": "Jornada Fin de Semana",
                    "horas_semanales": 20
                },
                {
                    "nombre": "Jornada de Práctica",
                    "horas_semanales": 30
                },
                {
                    "nombre": "Jornada de Capacitación",
                    "horas_semanales": 25
                },
                {
                    "nombre": "Jornada Especial Discapacidad",
                    "horas_semanales": 30
                }
            ]

            jornadas_creadas = 0

            for jornada_data in jornadas_data:
                try:
                    # Buscar por nombre (campo único)
                    jornada_obj, created = jornada.objects.get_or_create(
                        nombre=jornada_data["nombre"],
                        defaults={
                            "horas_semanales": jornada_data["horas_semanales"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        jornadas_creadas += 1
                        self.stdout.write(f"Jornada creada: {jornada_data['nombre']} ({jornada_data['horas_semanales']} horas semanales)")
                    else:
                        # Actualizar jornada existente si las horas cambiaron
                        if jornada_obj.horas_semanales != jornada_data["horas_semanales"]:
                            jornada_obj.horas_semanales = jornada_data["horas_semanales"]
                            jornada_obj.save()
                            self.stdout.write(f"Jornada actualizada: {jornada_data['nombre']} ({jornada_data['horas_semanales']} horas semanales)")
                        else:
                            self.stdout.write(f"Jornada existente: {jornada_data['nombre']}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando jornada {jornada_data['nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(jornadas_data)} jornadas, {jornadas_creadas} nuevas creadas"))