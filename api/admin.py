from django.contrib import admin
from .models import Activo, Riesgo, CatalogoAmenaza, CatalogoVulnerabilidad
# (deja tus otros registros existentes si ya tienes)

admin.site.register(CatalogoAmenaza)
admin.site.register(CatalogoVulnerabilidad)