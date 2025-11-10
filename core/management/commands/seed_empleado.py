# core/management/commands/seed_empleados.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from core.models import empleado, ZonaTrabajo, cargo

User = get_user_model()

ADMIN_USERNAME = "admin.rh"
ADMIN_PASSWORD = "temp123456"

class Command(BaseCommand):
    help = "Siembra datos iniciales para empleados (admin + no-admin)"

    def handle(self, *args, **options):
        with transaction.atomic():
            grp_admin, _ = Group.objects.get_or_create(name="Admin")
            grp_emp, _ = Group.objects.get_or_create(name="Empleado")

            empleados_data = [
                {
                    "username": "admin.rh",
                    "email": "admin.rh@empresa.com",
                    "first_name": "Ana",
                    "last_name": "González López",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "12.345.678-9",
                        "fono": 912345678,
                        "nacionalidad": "Chilena",
                        "zona": "Oficina Central - Piso 2",
                        "cargo": "Gerente de Recursos Humanos",
                    },
                },
                {
                    "username": "maria.contreras",
                    "email": "maria.contreras@empresa.com",
                    "first_name": "María",
                    "last_name": "Contreras Silva",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "13.456.789-0",
                        "fono": 922334455,
                        "nacionalidad": "Chilena",
                        "zona": "Sala de Reuniones - Piso 1",
                        "cargo": "Contador General",
                    },
                },
                {
                    "username": "carlos.munoz",
                    "email": "carlos.munoz@empresa.com",
                    "first_name": "Carlos",
                    "last_name": "Muñoz Rojas",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "14.567.890-1",
                        "fono": 933445566,
                        "nacionalidad": "Chilena",
                        "zona": "Área de Capacitación",
                        "cargo": "Gerente de TI",
                    },
                },
                {
                    "username": "juan.perez",
                    "email": "juan.perez@empresa.com",
                    "first_name": "Juan",
                    "last_name": "Pérez Martínez",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "15.678.901-2",
                        "fono": 944556677,
                        "nacionalidad": "Chilena",
                        "zona": "Oficina Contabilidad",
                        "cargo": "Analista Financiero",
                    },
                },
                {
                    "username": "laura.torres",
                    "email": "laura.torres@empresa.com",
                    "first_name": "Laura",
                    "last_name": "Torres Díaz",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "16.789.012-3",
                        "fono": 955667788,
                        "nacionalidad": "Chilena",
                        "zona": "Sala de Descanso",
                        "cargo": "Desarrollador Senior",
                    },
                },
                {
                    "username": "roberto.sanchez",
                    "email": "roberto.sanchez@empresa.com",
                    "first_name": "Roberto",
                    "last_name": "Sánchez Vargas",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "17.890.123-4",
                        "fono": 966778899,
                        "nacionalidad": "Chilena",
                        "zona": "Centro de Operaciones TI",
                        "cargo": "Jefe de Departamento",
                    },
                },
                {
                    "username": "patricia.mendoza",
                    "email": "patricia.mendoza@empresa.com",
                    "first_name": "Patricia",
                    "last_name": "Mendoza Castro",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "18.901.234-5",
                        "fono": 977889900,
                        "nacionalidad": "Chilena",
                        "zona": "Oficina Ventas",
                        "cargo": "Ejecutivo de Ventas",
                    },
                },
                {
                    "username": "miguel.herrera",
                    "email": "miguel.herrera@empresa.com",
                    "first_name": "Miguel",
                    "last_name": "Herrera Flores",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "19.012.345-6",
                        "fono": 988990011,
                        "nacionalidad": "Chilena",
                        "zona": "Laboratorio Desarrollo",
                        "cargo": "Analista de RH",
                    },
                },
                {
                    "username": "daniela.rios",
                    "email": "daniela.rios@empresa.com",
                    "first_name": "Daniela",
                    "last_name": "Ríos Navarro",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "20.123.456-7",
                        "fono": 999001122,
                        "nacionalidad": "Chilena",
                        "zona": "Laboratorio Desarrollo",
                        "cargo": "Asistente Administrativo",
                    },
                },
                {
                    "username": "fernando.guzman",
                    "email": "fernando.guzman@empresa.com",
                    "first_name": "Fernando",
                    "last_name": "Guzmán Ortega",
                    "password": "temp123456",
                    "empleado_data": {
                        "run": "21.234.567-8",
                        "fono": 911223344,
                        "nacionalidad": "Chilena",
                        "zona": "Oficina Ventas",
                        "cargo": "Administrador de Sistemas",
                    },
                },
            ]

            empleados_creados = 0

            for emp_data in empleados_data:
                try:
                    # crear o actualizar usuario
                    user, user_created = User.objects.get_or_create(
                        username=emp_data["username"],
                        defaults={
                            "email": emp_data["email"],
                            "first_name": emp_data["first_name"],
                            "last_name": emp_data["last_name"],
                            "is_active": True,
                        },
                    )

                    user.email = emp_data["email"]
                    user.first_name = emp_data["first_name"]
                    user.last_name = emp_data["last_name"]
                    user.set_password(emp_data["password"])

                    if emp_data["username"] == ADMIN_USERNAME:
                        user.is_staff = True
                        user.is_superuser = True
                    else:
                        user.is_staff = False
                        user.is_superuser = False

                    user.save()

                    # asignar grupo
                    if emp_data["username"] == ADMIN_USERNAME:
                        user.groups.add(grp_admin)
                        user.groups.remove(grp_emp)
                    else:
                        user.groups.add(grp_emp)
                        user.groups.remove(grp_admin)

                    # --- Resolver zona ---
                    zona_nombre = emp_data["empleado_data"].get("zona")
                    z = None
                    if zona_nombre:
                        try:
                            z = ZonaTrabajo.objects.get(nombre__iexact=zona_nombre)
                        except ZonaTrabajo.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f"Zona '{zona_nombre}' no existe. {emp_data['empleado_data']['run']} queda sin zona."
                            ))

                    # --- Resolver cargo ---
                    cargo_nombre = emp_data["empleado_data"].get("cargo")
                    cargo_obj = None
                    if cargo_nombre:
                        try:
                            cargo_obj = cargo.objects.get(nombre__iexact=cargo_nombre)
                        except cargo.DoesNotExist:
                            cargo_obj = cargo.objects.create(nombre=cargo_nombre, description="")
                            self.stdout.write(self.style.WARNING(
                                f"Cargo '{cargo_nombre}' no existía, creado automáticamente."
                            ))

                    # --- Crear/actualizar empleado ---
                    emp_obj, emp_created = empleado.objects.get_or_create(
                        run=emp_data["empleado_data"]["run"],
                        defaults={
                            "user": user,
                            "fono": emp_data["empleado_data"]["fono"],
                            "nacionalidad": emp_data["empleado_data"]["nacionalidad"],
                            "status": "ACTIVE",
                            "zona_trabajo": z,
                            "cargo": cargo_obj,
                        },
                    )

                    if not emp_created:
                        emp_obj.user = user
                        emp_obj.fono = emp_data["empleado_data"]["fono"]
                        emp_obj.nacionalidad = emp_data["empleado_data"]["nacionalidad"]
                        emp_obj.status = "ACTIVE"
                        if emp_obj.zona_trabajo_id != (z.id if z else None):
                            emp_obj.zona_trabajo = z
                        if emp_obj.cargo_id != (cargo_obj.id if cargo_obj else None):
                            emp_obj.cargo = cargo_obj
                        emp_obj.save()
                        self.stdout.write(f"Empleado actualizado: {emp_data['first_name']} {emp_data['last_name']}")
                    else:
                        empleados_creados += 1
                        self.stdout.write(f"Empleado creado: {emp_data['first_name']} {emp_data['last_name']} (RUN: {emp_data['empleado_data']['run']})")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando empleado {emp_data['username']}: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(empleados_data)} usuarios; empleados nuevos: {empleados_creados}"))
