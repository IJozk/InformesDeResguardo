import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
from typing import Tuple


def calculate_distance_to_roads(latitude: float, longitude: float, shapefile_path: Path) -> Tuple[float, bool]:
    """
    Calcula distancia de un punto al camino más cercano.
    
    Args:
        latitude: Latitud del punto
        longitude: Longitud del punto
        shapefile_path: Path al shapefile de caminos
    
    Returns:
        Tupla (distancia_en_metros, is_safe)
        - distancia_en_metros: float
        - is_safe: True si >= 50m, False si < 50m
    """
    # Cargar shapefile de caminos
    roads = gpd.read_file(shapefile_path)
    
    # Crear punto desde coordenadas (WGS84 / EPSG:4326)
    point = gpd.GeoSeries([Point(longitude, latitude)], crs="EPSG:4326")
    
    # Reproyectar a UTM zona 19S (Chile sur) para cálculos en metros
    roads_utm = roads.to_crs("EPSG:32719")
    point_utm = point.to_crs("EPSG:32719")
    
    # Calcular distancia al camino más cercano
    min_distance = roads_utm.distance(point_utm[0]).min()
    
    # Determinar si es seguro (>= 50 metros)
    is_safe = min_distance >= 50.0
    
    return float(min_distance), is_safe