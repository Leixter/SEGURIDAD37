from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ─────────────────────────────────────────
# Tablas de parámetros / catálogos
# ─────────────────────────────────────────

class ParamEstadoActivo(models.Model):
    """Param_Estados_Activo"""
    id_estado_activo = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=100)

    class Meta:
        db_table = "Param_Estados_Activo"
        verbose_name = "Estado de Activo"
        verbose_name_plural = "Estados de Activos"

    def __str__(self):
        return self.nombre_estado


class ParamTipoActivo(models.Model):
    """Param_Tipos_Activo"""
    id_tipo_activo = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    nombre_tipo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    ejemplo = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Param_Tipos_Activo"
        verbose_name = "Tipo de Activo"
        verbose_name_plural = "Tipos de Activos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre_tipo}"


class ParamTipoUbicacion(models.Model):
    """Param_Tipos_Ubicacion"""
    id_tipo_ubicacion = models.AutoField(primary_key=True)
    nombre_ubicacion = models.CharField(max_length=100)

    class Meta:
        db_table = "Param_Tipos_Ubicacion"
        verbose_name = "Tipo de Ubicación"
        verbose_name_plural = "Tipos de Ubicaciones"

    def __str__(self):
        return self.nombre_ubicacion


class CatalogoISO(models.Model):
    """Catalogo_ISO"""
    id_control = models.CharField(max_length=20, primary_key=True)
    norma = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100)
    titulo_control = models.CharField(max_length=250)
    descripcion = models.TextField()

    class Meta:
        db_table = "Catalogo_ISO"
        verbose_name = "Control ISO"
        verbose_name_plural = "Catálogo ISO"

    def __str__(self):
        return f"{self.id_control} - {self.titulo_control}"


# ─────────────────────────────────────────
# Activos
# ─────────────────────────────────────────

class Activo(models.Model):
    """Activos"""
    id_activo = models.AutoField(primary_key=True)
    nombre_activo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    sistema_involucrado = models.CharField(max_length=100)
    id_tipo_activo = models.ForeignKey(
        ParamTipoActivo,
        on_delete=models.RESTRICT,
        db_column="id_tipo_activo",
        related_name="activos",
    )
    id_tipo_ubicacion = models.ForeignKey(
        ParamTipoUbicacion,
        on_delete=models.RESTRICT,
        db_column="id_tipo_ubicacion",
        related_name="activos",
    )
    id_estado_activo = models.ForeignKey(
        ParamEstadoActivo,
        on_delete=models.RESTRICT,
        db_column="id_estado_activo",
        related_name="activos",
    )
    id_propietario = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column="id_propietario",
        related_name="activos_propietario",
    )
    sensibilidad = models.IntegerField(null=True, blank=True)
    funcion_activo = models.CharField(max_length=200, null=True, blank=True)
    area_trabajo = models.CharField(max_length=100, null=True, blank=True)
    cargo_administrative = models.CharField(max_length=100, null=True, blank=True)
    confidencialidad = models.IntegerField()
    integridad = models.IntegerField()
    disponibilidad = models.IntegerField()
    valor_final_max = models.IntegerField(null=True, blank=True)
    nivel_impacto = models.IntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "Activos"
        verbose_name = "Activo"
        verbose_name_plural = "Activos"
        indexes = [
            models.Index(fields=["id_propietario"], name="IX_Activos_Propietario"),
        ]

    def __str__(self):
        return self.nombre_activo


# ─────────────────────────────────────────
# Controles de la Empresa
# ─────────────────────────────────────────

class ControlEmpresa(models.Model):
    """Controles_Empresa"""
    id_control_emp = models.AutoField(primary_key=True)
    nombre_control = models.CharField(max_length=150)
    id_iso_padre = models.ForeignKey(
        CatalogoISO,
        on_delete=models.RESTRICT,
        db_column="id_iso_padre",
        to_field="id_control",
        related_name="controles_empresa",
    )
    naturaleza_valor = models.IntegerField()
    ejecucion_valor = models.IntegerField()
    documentacion_valor = models.IntegerField()
    eficacia_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "Controles_Empresa"
        verbose_name = "Control de Empresa"
        verbose_name_plural = "Controles de Empresa"

    def __str__(self):
        return self.nombre_control


# ─────────────────────────────────────────
# Riesgos
# ─────────────────────────────────────────


# ─────────────────────────────────────────
# Catálogos de Amenaza y Vulnerabilidad
# ─────────────────────────────────────────

class CatalogoAmenaza(models.Model):
    id_amenaza = models.AutoField(primary_key=True)
    nombre_amenaza = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Catalogo_Amenazas"
        verbose_name = "Amenaza"
        verbose_name_plural = "Catálogo de Amenazas"

    def __str__(self):
        return self.nombre_amenaza


class CatalogoVulnerabilidad(models.Model):
    id_vulnerabilidad = models.AutoField(primary_key=True)
    nombre_vulnerabilidad = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Catalogo_Vulnerabilidades"
        verbose_name = "Vulnerabilidad"
        verbose_name_plural = "Catálogo de Vulnerabilidades"

    def __str__(self):
        return self.nombre_vulnerabilidad

class Riesgo(models.Model):
    """Riesgos"""
    id_riesgo = models.AutoField(primary_key=True)
    id_activo = models.ForeignKey(
        Activo, on_delete=models.CASCADE, db_column="id_activo", related_name="riesgos",
    )
    nombre_riesgo = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)

    # --- NUEVO: Amenaza (catálogo + opción "otro") ---
    id_amenaza = models.ForeignKey(
        CatalogoAmenaza, on_delete=models.SET_NULL, null=True, blank=True,
        db_column="id_amenaza", related_name="riesgos",
    )
    amenaza_otro = models.CharField(max_length=200, null=True, blank=True)

    # --- NUEVO: Vulnerabilidad (catálogo + opción "otro") ---
    id_vulnerabilidad_cat = models.ForeignKey(
        CatalogoVulnerabilidad, on_delete=models.SET_NULL, null=True, blank=True,
        db_column="id_vulnerabilidad_cat", related_name="riesgos",
    )
    vulnerabilidad_otro = models.CharField(max_length=200, null=True, blank=True)

    nivel_probabilidad = models.IntegerField()
    nivel_vulnerabilidad = models.IntegerField()
    score_inherente = models.IntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "Riesgos"
        verbose_name = "Riesgo"
        verbose_name_plural = "Riesgos"
        indexes = [models.Index(fields=["id_activo"], name="IX_Riesgos_Activo")]

    def __str__(self):
        return self.nombre_riesgo

# ─────────────────────────────────────────
# Tratamiento de Riesgo
# ─────────────────────────────────────────

class TratamientoRiesgo(models.Model):
    """Tratamiento_Riesgo"""
    id_treatment = models.AutoField(primary_key=True)
    id_riesgo = models.ForeignKey(
        Riesgo,
        on_delete=models.CASCADE,
        db_column="id_riesgo",
        related_name="tratamientos",
    )
    id_control_emp = models.ForeignKey(
        ControlEmpresa,
        on_delete=models.RESTRICT,
        db_column="id_control_emp",
        related_name="tratamientos",
    )
    estrategia = models.CharField(max_length=50)
    probabilidad_residual = models.IntegerField()
    impacto_residual = models.IntegerField()
    score_residual = models.IntegerField(null=True, blank=True)
    nivel_residual = models.CharField(max_length=20, null=True, blank=True)
    id_responsable = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column="id_responsable",
        related_name="tratamientos_responsable",
    )
    observaciones = models.TextField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    es_activo = models.BooleanField(default=True)

    class Meta:
        db_table = "Tratamiento_Riesgo"
        verbose_name = "Tratamiento de Riesgo"
        verbose_name_plural = "Tratamientos de Riesgo"
        indexes = [
            models.Index(fields=["id_riesgo"], name="IX_Tratamiento_Riesgo"),
            models.Index(fields=["id_responsable"], name="IX_Tratamiento_Responsable"),
        ]

    def __str__(self):
        return f"Tratamiento #{self.id_treatment} - {self.estrategia}"


# ─────────────────────────────────────────
# Historial de Tratamiento de Riesgo
# ─────────────────────────────────────────

class HistorialTratamientoRiesgo(models.Model):
    """Historial_Tratamiento_Riesgo"""
    id_historial = models.AutoField(primary_key=True)
    id_treatment = models.ForeignKey(
        TratamientoRiesgo,
        on_delete=models.DO_NOTHING,
        db_column="id_treatment",
        related_name="historial",
    )
    id_riesgo = models.ForeignKey(
        Riesgo,
        on_delete=models.DO_NOTHING,
        db_column="id_riesgo",
        related_name="historial",
    )
    probabilidad_registrada = models.IntegerField()
    impacto_registrado = models.IntegerField()
    score_registrado = models.IntegerField(null=True, blank=True)
    nivel_registrado = models.CharField(max_length=20, null=True, blank=True)
    descripcion_cambio = models.CharField(max_length=500, null=True, blank=True)
    id_usuario_cambio = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column="id_usuario_cambio",
        related_name="historial_cambios",
    )
    fecha_cambio = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "Historial_Tratamiento_Riesgo"
        verbose_name = "Historial de Tratamiento"
        verbose_name_plural = "Historial de Tratamientos"
        indexes = [
            models.Index(fields=["fecha_cambio"], name="IX_Historial_Fecha"),
            models.Index(fields=["id_riesgo"], name="IX_Historial_Riesgo"),
        ]

    def __str__(self):
        return f"Historial #{self.id_historial} - {self.fecha_cambio}"