from ninja import Schema
from datetime import datetime


class LocationSchema(Schema):
    """
    Representa la ubicación geográfica en el JSON de salida.
    Este es un objeto anidado dentro de SafeguardReportOutSchema.
    """
    latitude: float
    longitude: float


class SafeguardReportOutSchema(Schema):
    """
    Define el formato EXACTO del JSON de salida para GET /safeguard-reports/
    Debe coincidir 100% con lo que pide el desafío.
    """
    id: int
    machine_serial: str
    report_datetime: datetime
    engine_off_timestamp: datetime
    is_safe: bool
    location: LocationSchema  # Objeto anidado
    distance_to_road_m: float
    is_active: bool


class SafeguardReportUpdateSchema(Schema):
    """
    Define qué acepta el PATCH /safeguard-reports/{id}/
    Solo permite cambiar is_active (soft delete).
    """
    is_active: bool


class ProcessingResponseSchema(Schema):
    """
    Respuesta simple para POST /data-processing/
    Solo confirma que el procesamiento comenzó.
    """
    message: str