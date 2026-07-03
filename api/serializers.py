from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CatalogoISO, ControlEmpresa, TratamientoRiesgo, HistorialTratamientoRiesgo
from .models import CatalogoAmenaza, CatalogoVulnerabilidad  # añade al import existente
from .models import (
    ParamEstadoActivo, ParamTipoActivo, ParamTipoUbicacion,
    CatalogoISO, Activo, ControlEmpresa, Riesgo, 
    TratamientoRiesgo, HistorialTratamientoRiesgo
)

class ParamTiposActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParamTipoActivo
        fields = '__all__'

class ActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activo
        fields = '__all__'

class HistorialTratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialTratamientoRiesgo
        fields = '__all__'

class CatalogoAmenazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoAmenaza
        fields = '__all__'

class CatalogoVulnerabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoVulnerabilidad
        fields = '__all__'

class RiesgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riesgo
        fields = '__all__'

class CatalogoISOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoISO
        fields = '__all__'

class ControlEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlEmpresa
        fields = '__all__'

class TratamientoRiesgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamientoRiesgo
        fields = '__all__'

class HistorialTratamientoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = HistorialTratamientoRiesgo
        fields = '__all__'