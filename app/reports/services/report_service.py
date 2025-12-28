from typing import List
from ..models import SafeguardReport
from django.utils import timezone

def list_active_reports() -> List[SafeguardReport]:
    """
    Retorna todos los reportes activos ordenados por fecha.
    """
    return SafeguardReport.objects.filter(is_active=True)

def get_report_by_id(report_id: int) -> SafeguardReport:
    """
    Obtiene un reporte por ID.
    Lanza DoesNotExist si no existe.
    """
    return SafeguardReport.objects.get(id=report_id)

def create_report(
    machine_serial: str,
    engine_off_timestamp,
    latitude: float,
    longitude: float,
    distance_to_road_m: float,
    is_safe: bool
) -> SafeguardReport:
    """
    Crea un nuevo reporte de resguardo.
    
    Args:
        machine_serial: Número de serie de la máquina
        engine_off_timestamp: Timestamp cuando se apagó el motor
        latitude: Latitud de la ubicación
        longitude: Longitud de la ubicación
        distance_to_road_m: Distancia al camino en metros
        is_safe: True si >= 50m, False si < 50m
    
    Returns:
        SafeguardReport creado
    """
    report = SafeguardReport.objects.create(
        machine_serial=machine_serial,
        report_datetime=timezone.now(),  # Momento de creación del reporte
        engine_off_timestamp=engine_off_timestamp,
        latitude=latitude,
        longitude=longitude,
        distance_to_road_m=distance_to_road_m,
        is_safe=is_safe,
        is_active=True
    )
    return report

def update_report_status(report_id: int, is_active: bool) -> SafeguardReport:
    """
    Actualiza el estado is_active de un reporte (soft delete).
    
    Args:
        report_id: ID del reporte
        is_active: Nuevo estado
    
    Returns:
        SafeguardReport actualizado
    """
    report = get_report_by_id(report_id)
    report.is_active = is_active
    report.save()
    return report

def delete_all_reports():
    """
    Elimina todos los reportes (útil para testing).
    """
    SafeguardReport.objects.all().delete()
