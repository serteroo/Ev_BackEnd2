# core/management/commands/seed_all.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Ejecuta todas las semillas en orden"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando siembra completa...")
        
        # NOMBRES EN SINGULAR (como están en tu BD)
        commands = [
            'seed_rol',              # ← singular
            'seed_departamento',     # ← singular  
            'seed_cargo',            # ← singular
            'seed_turno',            # ← singular
            'seed_jornada',          # ← singular
            'seed_turno_jornada',    # ← este está bien
            'seed_forma_pago',       # ← singular
            'seed_direccion',        # ← singular
            'seed_empleado',         # ← singular
            'seed_cuenta_bancarias', # ← este está bien (plural correcto)
            'seed_contrato',         # ← singular
            'seed_liquidacion',      # ← singular
            'seed_pago',             # ← singular
        ]

        for command in commands:
            try:
                self.stdout.write(f"📦 Ejecutando: {command}")
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f"✅ {command} completado"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error en {command}: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS("🎉 Siembra completa finalizada"))