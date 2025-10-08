from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    STATUS = [("ACTIVE", "Active"), ("INACTIVE", "Inactive")]
    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True) 


    class Meta:
        abstract = True 

class direccion(BaseModel):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    depto = models.CharField(max_length=10, blank=True, null=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'direccion'
        managed = True

class roles(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'roles'
        managed = True

class departamento(BaseModel):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'departamento'
        managed = True

class cargo(BaseModel):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'cargo'
        managed = True
class empleado(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run = models.CharField(max_length=45, unique=True)
    fono = models.IntegerField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'empleado'
        managed = True

class cuenta_bancaria(BaseModel):
    banco = models.CharField(max_length=45)
    tipo_cuenta = models.CharField(max_length=45)
    numero_cuenta = models.BigIntegerField()
    correo = models.CharField(max_length=45, blank=True, null=True)
    empleado = models.ForeignKey('empleado', on_delete=models.DO_NOTHING, db_column='empleado_id', related_name='cuentas_bancarias')

    class Meta:
        db_table = 'cuenta_bancaria'
        managed = True


class turno(BaseModel):
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    class Meta:
        db_table = 'turno'
        managed =  True

class jornada(BaseModel):
    nombre = models.CharField(max_length=45)
    horas_semanales = models.IntegerField()

    class Meta:
        db_table = 'jornada'
        managed = True

class turno_has_jornada(BaseModel):
    turno = models.ForeignKey('turno', on_delete=models.DO_NOTHING, db_column='turno_id')
    jornada = models.ForeignKey('jornada', on_delete=models.DO_NOTHING, db_column='jornada_id')

    class Meta:
        db_table = 'turno_has_jornada'
        managed = True
        unique_together = (('turno', 'jornada'),)

class contrato(BaseModel):
    detalle_contrato = models.CharField(max_length=45, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    empleado = models.ForeignKey('empleado', on_delete=models.DO_NOTHING, db_column='empleado_id')
    cargo = models.ForeignKey('cargo', on_delete=models.DO_NOTHING, db_column='cargo_id')
    departamento = models.ForeignKey('departamento', on_delete=models.DO_NOTHING, db_column='departamento_id')
    turno_has_jornada = models.ForeignKey('turno_has_jornada', on_delete=models.DO_NOTHING, db_column='turno_has_jornada_id')

    class Meta:
        db_table = 'contrato'
        managed = True

class liquidacion(BaseModel):
    periodo = models.DateField()
    fecha_pago = models.DateField(blank=True, null=True)

    imponible = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    no_imponible = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tributable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuentos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anticipo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    liquido = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    devengado = models.DateField(blank=True, null=True)
    cierre = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=45)

    contrato = models.ForeignKey('contrato', on_delete=models.DO_NOTHING, db_column='contrato_id')

    class Meta:
        db_table = 'liquidacion'
        managed = True

class forma_pago(BaseModel):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'forma_pago'
        managed = True

class pago(BaseModel):
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    comprobante = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=45)

    liquidacion = models.ForeignKey('liquidacion', on_delete=models.DO_NOTHING, db_column='liquidacion_id', related_name='pagos')
    forma_pago = models.ForeignKey('forma_pago', on_delete=models.DO_NOTHING, db_column='forma_pago_id')

    class Meta:
        db_table = 'pago'
        managed = True

