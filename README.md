# InformesDeResguardo

Microservicio con stack tecnológico python para proceso de datos de telemetría prueba técnica.


### Prerrequisitos

* Docker y Docker Compose instalados
* Git (opcional, para clonar el repo)

### Pasos

**1. Clonar o descargar el proyecto**

```bash
git clone <url-repo>
cd InformesDeResguardo
```

**2. Verificar que existan los archivos de datos** Los XMLs y shapefile deben estar en `instrucciones/`:

* `LocationMessages-844585-page_1.xml`
* `LocationMessages-844585-page_2.xml`
* `EngineStatusMessages-844585.xml`
* `CAMINOS_7336.shp` (+ .shx, .dbf, .prj, etc.)

**3. Construir y levantar el contenedor**

```bash
docker-compose up --build
```

Espera a ver:

```
safeguard_api  | Running migrations...
safeguard_api  | Starting server...
safeguard_api  | Django version 5.x.x, using settings 'config.settings'
safeguard_api  | Starting development server at http://0.0.0.0:8000/
```

**4. Procesar los datos**

```bash
curl -X POST http://localhost:8000/api/data-processing/
```

Respuesta esperada:

```json
{"message": "Data processing initiated successfully."}
```

**5. Consultar reportes generados**

```bash
curl http://localhost:8000/api/safeguard-reports/
```

**6. Soft delete de un reporte**

```bash
curl -X PATCH http://localhost:8000/api/safeguard-reports/1/ \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

### Comandos Útiles

**Detener el contenedor:**

```bash
docker-compose down
```

**Ver logs:**

```bash
docker-compose logs -f
```

**Reconstruir (si cambias código):**

```bash
docker-compose down
docker-compose up --build
```

**Acceder al contenedor:**

```bash
docker exec -it safeguard_api bash
```

### Endpoints Disponibles

* `POST /api/data-processing/` - Procesar XMLs
* `GET /api/safeguard-reports/` - Listar reportes activos
* `PATCH /api/safeguard-reports/{id}/` - Actualizar estado
* `GET /api/docs` - Documentación Swagger

---
