from rest_framework import serializers
from core.models import ZonaTrabajo, pago

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
         model = ZonaTrabajo
         fields = '__all__'


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pago
        fields = '__all__'
