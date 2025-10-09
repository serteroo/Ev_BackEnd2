# empleados/management/commands/seed_direcciones.py
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import direccion

class Command(BaseCommand):
    help = "Siembra datos iniciales para direcciones"

    def handle(self, *args, **options):
        with transaction.atomic():
            direcciones = [
                {
                    "calle": "Av. Libertador Bernardo O'Higgins",
                    "numero": "123",
                    "depto": "501",
                    "comuna": "Santiago",
                    "region": "Región Metropolitana",
                    "codigo_postal": "8320000"
                },
                {
                    "calle": "Av. Providencia",
                    "numero": "2456",
                    "depto": None,
                    "comuna": "Providencia", 
                    "region": "Región Metropolitana",
                    "codigo_postal": "7500000"
                },
                {
                    "calle": "Av. Kennedy",
                    "numero": "5423",
                    "depto": "302",
                    "comuna": "Las Condes",
                    "region": "Región Metropolitana", 
                    "codigo_postal": "7550000"
                },
                {
                    "calle": "Av. Vitacura",
                    "numero": "2890",
                    "depto": "1501",
                    "comuna": "Vitacura",
                    "region": "Región Metropolitana",
                    "codigo_postal": "7630000"
                },
                {
                    "calle": "Av. Santa María",
                    "numero": "5540",
                    "depto": None,
                    "comuna": "Recoleta",
                    "region": "Región Metropolitana",
                    "codigo_postal": "8420000"
                },
                {
                    "calle": "Av. Independencia",
                    "numero": "225",
                    "depto": "4A",
                    "comuna": "Independencia",
                    "region": "Región Metropolitana",
                    "codigo_postal": "8380000"
                },
                {
                    "calle": "Av. La Dehesa",
                    "numero": "1445",
                    "depto": "Casa 2",
                    "comuna": "Lo Barnechea",
                    "region": "Región Metropolitana", 
                    "codigo_postal": "7690000"
                },
                {
                    "calle": "Av. Tobalaba",
                    "numero": "1650",
                    "depto": "801",
                    "comuna": "Puente Alto",
                    "region": "Región Metropolitana",
                    "codigo_postal": "8160000"
                },
                {
                    "calle": "Av. Colón",
                    "numero": "3500",
                    "depto": None,
                    "comuna": "Valparaíso",
                    "region": "Región de Valparaíso",
                    "codigo_postal": "2340000"
                },
                {
                    "calle": "Av. Alemania",
                    "numero": "1098",
                    "depto": "B",
                    "comuna": "Temuco",
                    "region": "Región de La Araucanía",
                    "codigo_postal": "4780000"
                }
            ]

            for direccion_data in direcciones:
                # Buscar por combinación única de calle + numero + depto
                obj, created = direccion.objects.get_or_create(
                    calle=direccion_data["calle"],
                    numero=direccion_data["numero"],
                    depto=direccion_data["depto"],
                    defaults={
                        "comuna": direccion_data["comuna"],
                        "region": direccion_data["region"],
                        "codigo_postal": direccion_data["codigo_postal"],
                        "status": "ACTIVE"  # Heredado de BaseModel
                    }
                )
                
                if created:
                    self.stdout.write(f"Dirección creada: {direccion_data['calle']} {direccion_data['numero']}, {direccion_data['comuna']}")
                else:
                    # Actualizar si ya existe pero los datos cambiaron
                    obj.comuna = direccion_data["comuna"]
                    obj.region = direccion_data["region"]
                    obj.codigo_postal = direccion_data["codigo_postal"]
                    obj.status = "ACTIVE"
                    obj.save()
                    self.stdout.write(f"Dirección actualizada: {direccion_data['calle']} {direccion_data['numero']}")

        self.stdout.write(self.style.SUCCESS(f"Se sembraron {len(direcciones)} direcciones exitosamente"))