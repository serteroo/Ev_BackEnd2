from rest_framework import serializers
from core.models import ZonaTrabajo

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
         model = ZonaTrabajo
         fields = '__all__'
