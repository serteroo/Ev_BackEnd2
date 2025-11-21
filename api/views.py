from rest_framework import viewsets
from core.models import ZonaTrabajo, pago
from .serializers import ZonaSerializer, PagoSerializer
from django.http import JsonResponse



def health(request):
    return JsonResponse({"Proyecto": "Tarea BackEnd",
                         "version": "1.0.0",
                         "autor": "Renato Muñoz"})

def info(request):
    import platform
    import django
    import sys
    import pymysql

    info_data = {
        "python_version": sys.version,
        "django_version": django.get_version(),
        "pymysql_version": pymysql.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
    }
    return JsonResponse(info_data)

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = ZonaTrabajo.objects.all()
    serializer_class = ZonaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = pago.objects.all()
    serializer_class = PagoSerializer