# core/management/commands/seed_contratos.py
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta
from core.models import contrato, empleado, cargo, departamento, turno_has_jornada

class Command(BaseCommand):
    help = "Siembra datos iniciales para contratos"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Primero necesitamos obtener datos existentes
            empleados = empleado.objects.filter(status="ACTIVE")[:10]
            cargos_obj = cargo.objects.filter(status="ACTIVE")
            departamentos_obj = departamento.objects.filter(status="ACTIVE")
            turnos_jornadas = turno_has_jornada.objects.filter(status="ACTIVE")
            
            if not empleados.exists():
                self.stdout.write(self.style.ERROR("No hay empleados existentes. Ejecuta seed_empleados primero."))
                return
            if not cargos_obj.exists():
                self.stdout.write(self.style.ERROR("No hay cargos existentes. Ejecuta seed_cargos primero."))
                return
            if not departamentos_obj.exists():
                self.stdout.write(self.style.ERROR("No hay departamentos existentes. Ejecuta seed_departamentos primero."))
                return
            if not turnos_jornadas.exists():
                self.stdout.write(self.style.ERROR("No hay relaciones turno-jornada existentes. Ejecuta seed_turno_jornada primero."))
                return

            # Datos para contratos
            contratos_data = [
                {
                    "empleado_index": 0,  # admin.rh
                    "cargo_nombre": "Gerente de Recursos Humanos",
                    "departamento_nombre": "Recursos Humanos",
                    "turno_jornada_index": 0,  # Jornada Completa - Turno Mañana
                    "detalle_contrato": "Contrato Indefinido - Gerencia RH",
                    "fecha_inicio": date(2022, 3, 15),
                    "fecha_fin": None  # Indefinido
                },
                {
                    "empleado_index": 1,  # maria.contreras
                    "cargo_nombre": "Contador General",
                    "departamento_nombre": "Finanzas",
                    "turno_jornada_index": 1,  # Jornada Completa - Turno Tarde
                    "detalle_contrato": "Contrato Plazo Fijo 2 años",
                    "fecha_inicio": date(2023, 1, 10),
                    "fecha_fin": date(2025, 1, 10)
                },
                {
                    "empleado_index": 2,  # carlos.munoz
                    "cargo_nombre": "Gerente de TI",
                    "departamento_nombre": "Tecnología de la Información",
                    "turno_jornada_index": 2,  # Jornada Completa - Turno Ejecutivo
                    "detalle_contrato": "Contrato Indefinido - Gerencia TI",
                    "fecha_inicio": date(2022, 6, 1),
                    "fecha_fin": None
                },
                {
                    "empleado_index": 3,  # juan.perez
                    "cargo_nombre": "Analista Financiero",
                    "departamento_nombre": "Finanzas",
                    "turno_jornada_index": 0,  # Jornada Completa - Turno Mañana
                    "detalle_contrato": "Contrato Plazo Fijo 1 año",
                    "fecha_inicio": date(2024, 2, 1),
                    "fecha_fin": date(2025, 2, 1)
                },
                {
                    "empleado_index": 4,  # laura.torres
                    "cargo_nombre": "Desarrollador Senior",
                    "departamento_nombre": "Tecnología de la Información",
                    "turno_jornada_index": 4,  # Jornada Flexible - Turno Flexible Entrada
                    "detalle_contrato": "Contrato Indefinido - Desarrollador",
                    "fecha_inicio": date(2023, 8, 20),
                    "fecha_fin": None
                },
                {
                    "empleado_index": 5,  # roberto.sanchez
                    "cargo_nombre": "Jefe de Departamento",
                    "departamento_nombre": "Operaciones",
                    "turno_jornada_index": 0,  # Jornada Completa - Turno Mañana
                    "detalle_contrato": "Contrato Indefinido - Jefatura",
                    "fecha_inicio": date(2021, 11, 5),
                    "fecha_fin": None
                },
                {
                    "empleado_index": 6,  # patricia.mendoza
                    "cargo_nombre": "Ejecutivo de Ventas",
                    "departamento_nombre": "Ventas y Marketing",
                    "turno_jornada_index": 10,  # Jornada Comercial - Turno Comercial
                    "detalle_contrato": "Contrato Plazo Fijo 6 meses",
                    "fecha_inicio": date(2024, 1, 15),
                    "fecha_fin": date(2024, 7, 15)
                },
                {
                    "empleado_index": 7,  # miguel.herrera
                    "cargo_nombre": "Analista de RH",
                    "departamento_nombre": "Recursos Humanos",
                    "turno_jornada_index": 1,  # Jornada Completa - Turno Tarde
                    "detalle_contrato": "Contrato Indefinido - Analista",
                    "fecha_inicio": date(2023, 3, 10),
                    "fecha_fin": None
                },
                {
                    "empleado_index": 8,  # daniela.rios
                    "cargo_nombre": "Asistente Administrativo",
                    "departamento_nombre": "Administración",
                    "turno_jornada_index": 5,  # Jornada Parcial - Turno Partido Mañana
                    "detalle_contrato": "Contrato Medio Tiempo",
                    "fecha_inicio": date(2024, 3, 1),
                    "fecha_fin": date(2024, 9, 1)
                },
                {
                    "empleado_index": 9,  # fernando.guzman
                    "cargo_nombre": "Administrador de Sistemas",
                    "departamento_nombre": "Tecnología de la Información",
                    "turno_jornada_index": 13,  # Jornada por Turnos - 24/7 Grupo A
                    "detalle_contrato": "Contrato por Turnos - 24/7",
                    "fecha_inicio": date(2023, 12, 1),
                    "fecha_fin": None
                },
                # Contrato adicional para el primer empleado (cambio de cargo)
                {
                    "empleado_index": 0,  # admin.rh - contrato anterior
                    "cargo_nombre": "Analista de RH",
                    "departamento_nombre": "Recursos Humanos",
                    "turno_jornada_index": 1,  # Jornada Completa - Turno Tarde
                    "detalle_contrato": "Contrato Anterior - Analista RH",
                    "fecha_inicio": date(2020, 1, 15),
                    "fecha_fin": date(2022, 3, 14)
                }
            ]

            contratos_creados = 0

            for contrato_data in contratos_data:
                try:
                    # Obtener las instancias relacionadas
                    empleado_obj = empleados[contrato_data["empleado_index"]]
                    cargo_obj = cargos_obj.get(nombre=contrato_data["cargo_nombre"])
                    departamento_obj = departamentos_obj.get(nombre=contrato_data["departamento_nombre"])
                    turno_jornada_obj = turnos_jornadas[contrato_data["turno_jornada_index"]]
                    
                    # Crear el contrato
                    contrato_obj, created = contrato.objects.get_or_create(
                        empleado=empleado_obj,
                        fecha_inicio=contrato_data["fecha_inicio"],
                        defaults={
                            "detalle_contrato": contrato_data["detalle_contrato"],
                            "fecha_fin": contrato_data["fecha_fin"],
                            "cargo": cargo_obj,
                            "departamento": departamento_obj,
                            "turno_has_jornada": turno_jornada_obj,
                            "status": "ACTIVE"
                        }
                    )
                    
                    if created:
                        contratos_creados += 1
                        self.stdout.write(f"Contrato creado: {empleado_obj.user.get_full_name()} - {cargo_obj.nombre}")
                    else:
                        # Actualizar contrato existente
                        contrato_obj.detalle_contrato = contrato_data["detalle_contrato"]
                        contrato_obj.fecha_fin = contrato_data["fecha_fin"]
                        contrato_obj.cargo = cargo_obj
                        contrato_obj.departamento = departamento_obj
                        contrato_obj.turno_has_jornada = turno_jornada_obj
                        contrato_obj.status = "ACTIVE"
                        contrato_obj.save()
                        self.stdout.write(f"Contrato actualizado: {empleado_obj.user.get_full_name()}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando contrato: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(contratos_data)} contratos, {contratos_creados} nuevos creados"))