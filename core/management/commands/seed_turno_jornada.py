# core/management/commands/seed_turno_jornada.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import turno_has_jornada, turno, jornada

class Command(BaseCommand):
    help = "Siembra relaciones entre turnos y jornadas"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Primero necesitamos obtener turnos y jornadas existentes
            turnos = turno.objects.filter(status="ACTIVE")
            jornadas = jornada.objects.filter(status="ACTIVE")
            
            if not turnos.exists():
                self.stdout.write(self.style.ERROR("No hay turnos existentes. Ejecuta seed_turnos primero."))
                return
                
            if not jornadas.exists():
                self.stdout.write(self.style.ERROR("No hay jornadas existentes. Ejecuta seed_jornadas primero."))
                return

            # Definir relaciones lógicas entre turnos y jornadas
            relaciones_data = [
                # Jornada Completa - Turnos estándar
                {"turno_nombre": "Turno Mañana", "jornada_nombre": "Jornada Completa"},
                {"turno_nombre": "Turno Tarde", "jornada_nombre": "Jornada Completa"},
                {"turno_nombre": "Turno Ejecutivo", "jornada_nombre": "Jornada Completa"},
                
                # Jornada Parcial - Turnos partidos y flexibles
                {"turno_nombre": "Turno Partido Mañana", "jornada_nombre": "Jornada Parcial"},
                {"turno_nombre": "Turno Partido Tarde", "jornada_nombre": "Jornada Parcial"},
                {"turno_nombre": "Turno Flexible Entrada", "jornada_nombre": "Jornada Parcial"},
                {"turno_nombre": "Turno Flexible Salida", "jornada_nombre": "Jornada Parcial"},
                
                # Medio Tiempo - Turnos reducidos
                {"turno_nombre": "Turno Partido Mañana", "jornada_nombre": "Medio Tiempo"},
                {"turno_nombre": "Turno Partido Tarde", "jornada_nombre": "Medio Tiempo"},
                
                # Jornada Reducida
                {"turno_nombre": "Turno Flexible Entrada", "jornada_nombre": "Jornada Reducida"},
                {"turno_nombre": "Turno Flexible Salida", "jornada_nombre": "Jornada Reducida"},
                
                # Jornada Intensiva
                {"turno_nombre": "Turno Mañana", "jornada_nombre": "Jornada Intensiva"},
                {"turno_nombre": "Turno Tarde", "jornada_nombre": "Jornada Intensiva"},
                
                # Jornada por Turnos
                {"turno_nombre": "Turno 24/7 - Grupo A", "jornada_nombre": "Jornada por Turnos"},
                {"turno_nombre": "Turno 24/7 - Grupo B", "jornada_nombre": "Jornada por Turnos"},
                {"turno_nombre": "Turno 24/7 - Grupo C", "jornada_nombre": "Jornada por Turnos"},
                {"turno_nombre": "Turno Vespertino", "jornada_nombre": "Jornada por Turnos"},
                {"turno_nombre": "Turno Noche", "jornada_nombre": "Jornada por Turnos"},
                
                # Jornada Nocturna
                {"turno_nombre": "Turno Noche", "jornada_nombre": "Jornada Nocturna"},
                {"turno_nombre": "Turno Madrugada", "jornada_nombre": "Jornada Nocturna"},
                {"turno_nombre": "Turno 24/7 - Grupo C", "jornada_nombre": "Jornada Nocturna"},
                
                # Jornada Flexible
                {"turno_nombre": "Turno Flexible Entrada", "jornada_nombre": "Jornada Flexible"},
                {"turno_nombre": "Turno Flexible Salida", "jornada_nombre": "Jornada Flexible"},
                
                # Jornada Comercial
                {"turno_nombre": "Turno Comercial", "jornada_nombre": "Jornada Comercial"},
                
                # Jornada Operativa
                {"turno_nombre": "Turno 24/7 - Grupo A", "jornada_nombre": "Jornada Operativa"},
                {"turno_nombre": "Turno 24/7 - Grupo B", "jornada_nombre": "Jornada Operativa"},
                {"turno_nombre": "Turno 24/7 - Grupo C", "jornada_nombre": "Jornada Operativa"},
                
                # Jornada Fin de Semana
                {"turno_nombre": "Turno Mañana", "jornada_nombre": "Jornada Fin de Semana"},
                {"turno_nombre": "Turno Tarde", "jornada_nombre": "Jornada Fin de Semana"},
                
                # Jornadas Especiales
                {"turno_nombre": "Turno Partido Mañana", "jornada_nombre": "Jornada Estudiantil"},
                {"turno_nombre": "Turno Partido Tarde", "jornada_nombre": "Jornada de Práctica"},
                {"turno_nombre": "Turno Flexible Entrada", "jornada_nombre": "Jornada de Capacitación"},
            ]

            relaciones_creadas = 0

            for relacion_data in relaciones_data:
                try:
                    # Buscar turno y jornada por nombre
                    turno_obj = turnos.get(hora_entrada__icontains=relacion_data["turno_nombre"].split(" ")[1].lower())
                    jornada_obj = jornadas.get(nombre=relacion_data["jornada_nombre"])
                    
                    # Crear la relación (unique_together evita duplicados)
                    relacion_obj, created = turno_has_jornada.objects.get_or_create(
                        turno=turno_obj,
                        jornada=jornada_obj,
                        defaults={
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        relaciones_creadas += 1
                        self.stdout.write(f"Relación creada: {relacion_data['turno_nombre']} -> {relacion_data['jornada_nombre']}")
                    else:
                        self.stdout.write(f"Relación existente: {relacion_data['turno_nombre']} -> {relacion_data['jornada_nombre']}")

                except turno.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Turno no encontrado: {relacion_data['turno_nombre']}"))
                except jornada.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Jornada no encontrada: {relacion_data['jornada_nombre']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando relación {relacion_data['turno_nombre']} -> {relacion_data['jornada_nombre']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(relaciones_data)} relaciones, {relaciones_creadas} nuevas creadas"))