# core/management/commands/seed_turnos.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import turno
from datetime import time

class Command(BaseCommand):
    help = "Siembra datos iniciales para turnos"

    def handle(self, *args, **options):
        with transaction.atomic():
            turnos_data = [
                {
                    "nombre": "Turno Mañana",
                    "hora_entrada": time(8, 0),   # 08:00 AM
                    "hora_salida": time(17, 0)    # 05:00 PM
                },
                {
                    "nombre": "Turno Tarde",
                    "hora_entrada": time(9, 0),   # 09:00 AM
                    "hora_salida": time(18, 0)    # 06:00 PM
                },
                {
                    "nombre": "Turno Vespertino",
                    "hora_entrada": time(14, 0),  # 02:00 PM
                    "hora_salida": time(22, 0)    # 10:00 PM
                },
                {
                    "nombre": "Turno Noche",
                    "hora_entrada": time(22, 0),  # 10:00 PM
                    "hora_salida": time(6, 0)     # 06:00 AM
                },
                {
                    "nombre": "Turno Madrugada",
                    "hora_entrada": time(0, 0),   # 12:00 AM
                    "hora_salida": time(8, 0)     # 08:00 AM
                },
                {
                    "nombre": "Turno Partido Mañana",
                    "hora_entrada": time(7, 30),  # 07:30 AM
                    "hora_salida": time(12, 30)   # 12:30 PM
                },
                {
                    "nombre": "Turno Partido Tarde",
                    "hora_entrada": time(13, 0),  # 01:00 PM
                    "hora_salida": time(18, 0)    # 06:00 PM
                },
                {
                    "nombre": "Turno Flexible Entrada",
                    "hora_entrada": time(7, 0),   # 07:00 AM
                    "hora_salida": time(16, 0)    # 04:00 PM
                },
                {
                    "nombre": "Turno Flexible Salida",
                    "hora_entrada": time(10, 0),  # 10:00 AM
                    "hora_salida": time(19, 0)    # 07:00 PM
                },
                {
                    "nombre": "Turno Ejecutivo",
                    "hora_entrada": time(8, 30),  # 08:30 AM
                    "hora_salida": time(17, 30)   # 05:30 PM
                },
                {
                    "nombre": "Turno Comercial",
                    "hora_entrada": time(10, 0),  # 10:00 AM
                    "hora_salida": time(19, 0)    # 07:00 PM
                },
                {
                    "nombre": "Turno 24/7 - Grupo A",
                    "hora_entrada": time(6, 0),   # 06:00 AM
                    "hora_salida": time(14, 0)    # 02:00 PM
                },
                {
                    "nombre": "Turno 24/7 - Grupo B",
                    "hora_entrada": time(14, 0),  # 02:00 PM
                    "hora_salida": time(22, 0)    # 10:00 PM
                },
                {
                    "nombre": "Turno 24/7 - Grupo C",
                    "hora_entrada": time(22, 0),  # 10:00 PM
                    "hora_salida": time(6, 0)     # 06:00 AM
                }
            ]

            turnos_creados = 0

            for turno_data in turnos_data:
                try:
                    # Buscar por combinación de horarios (podría ser única)
                    turno_obj, created = turno.objects.get_or_create(
                        hora_entrada=turno_data["hora_entrada"],
                        hora_salida=turno_data["hora_salida"],
                        defaults={
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        turnos_creados += 1
                        self.stdout.write(f"Turno creado: {turno_data['nombre']} ({turno_data['hora_entrada'].strftime('%H:%M')} - {turno_data['hora_salida'].strftime('%H:%M')})")
                    else:
                        self.stdout.write(f"Turno existente: {turno_data['nombre']} ({turno_data['hora_entrada'].strftime('%H:%M')} - {turno_data['hora_salida'].strftime('%H:%M')})")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando turno {turno_data['nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(turnos_data)} turnos, {turnos_creados} nuevos creados"))