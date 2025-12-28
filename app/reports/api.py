from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import SafeguardReport
from .schemas import (
    SafeguardReportOutSchema,
    SafeguardReportUpdateSchema,
    ProcessingResponseSchema
)
from .services import report_service, processing_service  # <-- Agregar

router = Router()


@router.post("/data-processing/", response={202: ProcessingResponseSchema})
def process_data(request):
    """Inicia el procesamiento de datos de telemetría."""
    processing_service.process_all_data()  # <-- Llamar al service
    return 202, {"message": "Data processing initiated successfully."}


@router.get("/safeguard-reports/", response=List[SafeguardReportOutSchema])
def list_reports(request):
    """Lista todos los reportes activos."""
    reports = report_service.list_active_reports()  # <-- Usar service
    
    result = []
    for report in reports:
        result.append({
            "id": report.id,
            "machine_serial": report.machine_serial,
            "report_datetime": report.report_datetime,
            "engine_off_timestamp": report.engine_off_timestamp,
            "is_safe": report.is_safe,
            "location": {
                "latitude": float(report.latitude),
                "longitude": float(report.longitude)
            },
            "distance_to_road_m": report.distance_to_road_m,
            "is_active": report.is_active
        })
    
    return result


@router.patch("/safeguard-reports/{int:report_id}/", response=SafeguardReportOutSchema)
def update_report(request, report_id: int, payload: SafeguardReportUpdateSchema):
    """Actualiza el estado de un reporte (soft delete)."""
    report = report_service.update_report_status(report_id, payload.is_active)  # <-- Usar service
    
    return {
        "id": report.id,
        "machine_serial": report.machine_serial,
        "report_datetime": report.report_datetime,
        "engine_off_timestamp": report.engine_off_timestamp,
        "is_safe": report.is_safe,
        "location": {
            "latitude": float(report.latitude),
            "longitude": float(report.longitude)
        },
        "distance_to_road_m": report.distance_to_road_m,
        "is_active": report.is_active
    }
