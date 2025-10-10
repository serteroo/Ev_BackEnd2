# core/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = pago
        fields = "__all__"
        error_messages = {
            "monto": {"required": "El monto es obligatorio."},
            "fecha_pago": {"required": "La fecha de pago es obligatoria."},
        }

    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto is not None and monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")
        return monto

    def clean_fecha_pago(self):
        fecha = self.cleaned_data.get("fecha_pago")
        if not fecha:
            raise ValidationError("La fecha de pago es obligatoria.")
        return fecha
