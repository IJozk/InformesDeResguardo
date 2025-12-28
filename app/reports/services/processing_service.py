from pathlib import Path
from django.conf import settings
from . import report_service
from ..functions.xml_parser import parse_location_messages, parse_engine_status
from ..functions.safeguard_detector import identify_safeguards
from ..functions.distance_calculator import calculate_distance_to_roads


def process_all_data():
    """
    Proceso completo: parsea XMLs, identifica resguardos, calcula distancias, crea reportes.
    """
    # Definir rutas a los archivos
    data_dir = Path(settings.BASE_DIR) / 'data'
    
    location_files = [
        data_dir / 'LocationMessages-844585-page_1.xml',
        data_dir / 'LocationMessages-844585-page_2.xml'
    ]
    engine_file = data_dir / 'EngineStatusMessages-844585.xml'
    shapefile_path = data_dir / 'CAMINOS_7336.shp'
    
    # Paso 1: Parsear XMLs
    locations = parse_location_messages(location_files)
    engine_events = parse_engine_status(engine_file)
    
    # Paso 2: Identificar resguardos
    safeguards = identify_safeguards(engine_events)
    
    # Paso 3: Para cada resguardo, calcular distancia y guardar
    for safeguard in safeguards:
        # Encontrar ubicación más cercana en tiempo
        location = find_closest_location(locations, safeguard['timestamp'])
        
        # Calcular distancia al camino
        distance_m, is_safe = calculate_distance_to_roads(
            location['latitude'],
            location['longitude'],
            shapefile_path
        )
        
        # Crear reporte
        report_service.create_report(
            machine_serial=safeguard['machine_serial'],
            engine_off_timestamp=safeguard['timestamp'],
            latitude=location['latitude'],
            longitude=location['longitude'],
            distance_to_road_m=distance_m,
            is_safe=is_safe
        )


def find_closest_location(locations: list, target_timestamp) -> dict:
    """
    Encuentra la ubicación más cercana en tiempo a un timestamp dado.
    
    Args:
        locations: Lista de ubicaciones con timestamp
        target_timestamp: Timestamp objetivo
    
    Returns:
        Dict con latitude y longitude
    """
    closest = min(locations, key=lambda loc: abs((loc['timestamp'] - target_timestamp).total_seconds()))
    return closest
