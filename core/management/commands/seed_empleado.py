# core/management/commands/seed_empleados.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from core.models import empleado

class Command(BaseCommand):
    help = "Siembra datos iniciales para empleados"

    def handle(self, *args, **options):
        with transaction.atomic():
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
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
                        "nacionalidad": "Chilena"
                    }
                }
            ]

            empleados_creados = 0

            for emp_data in empleados_data:
                try:
                    # Crear o obtener el usuario
                    user, user_created = User.objects.get_or_create(
                        username=emp_data["username"],
                        defaults={
                            "email": emp_data["email"],
                            "first_name": emp_data["first_name"],
                            "last_name": emp_data["last_name"],
                            "is_staff": True,  # Para acceso al admin si es necesario
                            "is_active": True
                        }
                    )
                    
                    if user_created:
                        user.set_password(emp_data["password"])
                        user.save()
                        self.stdout.write(f"Usuario creado: {emp_data['username']}")
                    else:
                        self.stdout.write(f"Usuario existente: {emp_data['username']}")

                    # Crear o actualizar el empleado
                    empleado_obj, emp_created = empleado.objects.get_or_create(
                        run=emp_data["empleado_data"]["run"],
                        defaults={
                            "user": user,
                            "fono": emp_data["empleado_data"]["fono"],
                            "nacionalidad": emp_data["empleado_data"]["nacionalidad"],
                            "status": "ACTIVE"
                        }
                    )
                    
                    if emp_created:
                        empleados_creados += 1
                        self.stdout.write(f"Empleado creado: {emp_data['first_name']} {emp_data['last_name']} (RUN: {emp_data['empleado_data']['run']})")
                    else:
                        # Actualizar empleado existente
                        empleado_obj.user = user
                        empleado_obj.fono = emp_data["empleado_data"]["fono"]
                        empleado_obj.nacionalidad = emp_data["empleado_data"]["nacionalidad"]
                        empleado_obj.status = "ACTIVE"
                        empleado_obj.save()
                        self.stdout.write(f"Empleado actualizado: {emp_data['first_name']} {emp_data['last_name']}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando empleado {emp_data['username']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(empleados_data)} empleados, {empleados_creados} nuevos creados"))