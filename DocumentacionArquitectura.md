Requerimientos

- Docker desktop Version 4.55.0
- Python
- 


## Estructura del proyecto:

1. Models(models.py):
   * Se definen los reportes con sus campos requeridos.
   * Campos: id, machine_serial, report_datetiem, engine_off_timestamp, is_safe, latitude, longitude, distance_to_road_m, is_active (default = True)
2. Schemas(schemas.py):
   * Esquemas de entrada y salidad de las consultas al servicio.
   * Uso de Pydantic con Django Ninja.
3. API(api.py):
   * Se crearan 3 endpoints disponibles:
     1. Inicio de proceso de datos:
        * **Método y URL:** `POST /data-processing/`
        * No necesita body, solo inicia procesamiento de datos actuando como disparador.
        * Lógica del servidor:
          a. Localizar y leer archivos (LocationMessages y EngineStatusMessages).
          b. Identificar eventos de motor apagado fuera de horario (08:30 - 19:30).
          c. Calcular distancia en metros a la capa de caminos (resguardo inseguro para distancias > 50 m.).
          d. Crear y guardar informes de resguardo.
        * Respuesta de API: codigo de estado 202 Accepted y cuerto JSON simple que confirme inicio de procesamiento de datos.
          {
          "message": "Data processing initiated successfully."
          }
     2. Consulta de informe:
        * **Método y URL:** (`GET /safeguard-reports/`)
        * Lista los informes generados.
        * Respuesta, array de objetos JSON con la siguiente estructura:
          [
          {
          "id": 1,
          "machine_serial": "844585",
          "report_datetime": "2024-11-04T21:05:00Z",
          "engine_off_timestamp": "2024-11-04T20:05:00Z",
          "is_safe": false,
          "location": {
          "latitude": -37.12345,
          "longitude": -72.56789
          },
          "distance_to_road_m": 35.5,
          "is_active": true
          }
          ]
     3. Actualización de estado:
        * **Método y URL:** (`PATCH /safeguard-reports/{id}/`).
        * Permite borrado suave (soft delete).
        * Acepta cuerpo patch como `{ "is_active": false }`.
        * Ahora no se muestran aquellos informes como no activos.
4. Services (Capa de negocios)

    **
    `processing_service.py`** : Orquestador principal

* Metodo procces_all_data() que ejecuta:
  * Parseo de XMLs de ubicacion
  * Parseao de XMLs estado de motor
  * Identifica los resguardos
  * Calcula las distancias
  * Guarda los reportes en la DB

**
    `report_service.py`** : CRUD de reportes

5. Functions:
   * xml_parser.py:

     * `parse_location_messages()`: lee los 2 XMLs de ubicación, retorna lista de ubicaciones
     * `parse_engine_status()`: lee XML de estado de motor, retorna lista de eventos
   * safeguard_detector.py

     * `identify_safeguards(engine_events)`: filtra eventos de motor apagado fuera de horario (antes 08:30 o después 19:30)
     * Retorna lista de eventos de resguardo con timestamp
   * distance_calculator.py:

     * `calculate_distance_to_roads(lat, lon, shapefile_path)`: usa GeoPandas
     * Retorna distancia en metros
     * Determina is_safe (>= 50m)
6. Utils:
   * Funciones auxiliares para cargar shapefile
   * Conversiones de coordenadas si es necesario
   * Cualquier utilidad geoespacial reutilizable
