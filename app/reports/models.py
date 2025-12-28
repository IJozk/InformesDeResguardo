from django.db import models

# Create your models here.

class SafeguardReport(models.Model):
    """
    Modelo para almacenar informes de resguardo de máquinas forestales.
    Un resguardo ocurre cuando la máquina se apaga fuera del horario de turno.
    """
    
    # Identificador de la maquina
    machine_serial = models.CharField(  max_length=6, 
                                        help_text="Número de serie de la máquina" )

    # Timestamps
    report_datetime = models.DateTimeField( help_text="Fecha y hora del informe de resguardo" )
    engine_off_timestamp = models.DateTimeField( help_text="Fecha y hora en que se apagó el motor (evento de resguardo)" )

    # Ubicación
    latitude = models.DecimalField( max_digits=9,
                                    decimal_places=6, 
                                    help_text="Latitud de la ubicación del resguardo" )
    longitude = models.DecimalField( max_digits=9,
                                    decimal_places=6,
                                    help_text="Longitud de la ubicación del resguardo" )
    
    # Análisis de seguridad
    distance_to_road_m = models.FloatField( help_text="Distancia en metros al camino más cercano" )
    is_safe = models.BooleanField(
        help_text="True si el resguardo está a >= 50m de un camino, False si < 50m"
    )

    # Soft delete
    is_active = models.BooleanField(
        default=True,
        help_text="False indica que el registro fue eliminado (soft delete)"
    )
    
    # Metadata del modelo
    class Meta:
        db_table = 'safeguard_reports'
        ordering = ['-report_datetime']  # Más recientes primero
        indexes = [
            models.Index(fields=['machine_serial']),
            models.Index(fields=['is_active']),
            models.Index(fields=['-report_datetime']),
        ]

    def __str__(self):
        return f"Resguardo {self.machine_serial} - {self.report_datetime}"