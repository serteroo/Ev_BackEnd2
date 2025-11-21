from django.urls import path
from .views import health
from rest_framework import routers
from django.urls import path, include

from .views import health, info, ZoneViewSet, PagoViewSet
router = routers.DefaultRouter()
router.register(r'zonas', ZoneViewSet)
router.register(r'pago', PagoViewSet)




urlpatterns = [
     path('health/', health),
     path('Info/', info),
     path('', include(router.urls)),
]
