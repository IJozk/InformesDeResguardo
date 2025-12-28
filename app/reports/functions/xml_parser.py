import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
from pathlib import Path


def parse_location_messages(xml_files: List[Path]) -> List[Dict]:
    """
    Parsea archivos XML de ubicaciones.
    
    Args:
        xml_files: Lista de paths a archivos LocationMessages XML
    
    Returns:
        Lista de dicts con formato:
        [
            {
                'timestamp': datetime,
                'latitude': float,
                'longitude': float
            },
            ...
        ]
    """
    locations = []
    
    for xml_file in xml_files:
        # Parsear el XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Namespace del XML (ISO 15143-3)
        namespace = {'iso': 'http://standards.iso.org/iso/15143/-3'}
        
        # Encontrar todos los elementos <Location>
        for location_elem in root.findall('iso:Location', namespace):
            # Extraer atributo datetime
            datetime_str = location_elem.get('datetime')
            
            # Extraer Latitude y Longitude
            latitude_elem = location_elem.find('iso:Latitude', namespace)
            longitude_elem = location_elem.find('iso:Longitude', namespace)
            
            if datetime_str and latitude_elem is not None and longitude_elem is not None:
                locations.append({
                    'timestamp': datetime.fromisoformat(datetime_str.replace('Z', '+00:00')),
                    'latitude': float(latitude_elem.text),
                    'longitude': float(longitude_elem.text)
                })
    
    # Ordenar por timestamp (útil para búsquedas)
    locations.sort(key=lambda x: x['timestamp'])
    
    return locations


def parse_engine_status(xml_file: Path) -> List[Dict]:
    """
    Parsea archivo XML de estado del motor.
    
    Args:
        xml_file: Path al archivo EngineStatusMessages XML
    
    Returns:
        Lista de dicts con formato:
        [
            {
                'timestamp': datetime,
                'is_running': bool
            },
            ...
        ]
    """
    engine_events = []
    
    # Parsear el XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Namespace del XML
    namespace = {'iso': 'http://standards.iso.org/iso/15143/-3'}
    
    # Encontrar todos los elementos <EngineStatus>
    for engine_elem in root.findall('iso:EngineStatus', namespace):
        # Extraer atributo datetime
        datetime_str = engine_elem.get('datetime')
        
        # Extraer Running (true/false)
        running_elem = engine_elem.find('iso:Running', namespace)
        
        if datetime_str and running_elem is not None:
            is_running = running_elem.text.lower() == 'true'
            
            engine_events.append({
                'timestamp': datetime.fromisoformat(datetime_str.replace('Z', '+00:00')),
                'is_running': is_running
            })
    
    # Ordenar por timestamp
    engine_events.sort(key=lambda x: x['timestamp'])
    
    return engine_events
