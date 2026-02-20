# AFRelay: Microservicio de Facturación con integración a la Agencia Tributaria Argentina

<p align="center">
  <a href="https://github.com/NehuenLian/AFRelay/actions/workflows/tests.yml">
    <img src="https://github.com/NehuenLian/AFRelay/actions/workflows/tests.yml/badge.svg" alt="CI">
  </a>
  <a href="https://codecov.io/github/NehuenLian/AFRelay">
    <img src="https://img.shields.io/codecov/c/github/NehuenLian/AFRelay?label=coverage&token=20WL0URAGI" alt="coverage">
  </a>
</p>

<p align="center">
  <a href="https://af-relay-docs.vercel.app/intro">Documentacion</a>
  ·
  <a href="https://github.com/NehuenLian/AFRelay-E2E-Manual-tests">Repo de tests E2E</a>
</p>

**AFRelay** Es un middleware que evita al desarrollador tratar con el ecosistema XML y que permite comunicarse con AFIP como si fuera una API REST.  
**Control total**: Gratis. Sin modelo SaaS. Sin infraestructura Closed-Source.  
Sin la necesidad de que el desarrollador se involucre con SOAP.

- I/O de red asíncrono evita que el alto tiempo de respuesta del web service bloquee el event loop del servicio.
- Renueva el ticket de acceso cada 11 horas automáticamente y al levantar el servicio.
- No resuelve errores automaticamente ni los lanza, sólo devuelve información en forma de JSON.

### Requisitos

Para usar este servicio es necesario disponer de una clave fiscal, y utilizarla para obtener los certificados correspondientes para autenticarse ante los servicios web de AFIP/ARCA  
Los pasos a seguir para obtener los certificados se encuentran en la web oficial:
https://www.arca.gob.ar/ws/documentacion/certificados.asp

Una vez autenticado, el servicio web de autenticación entregará dos credenciales:
- Una clave privada con extensión "```.key```"
- Un certificado X.509 con extensión "```.pem```"

Se utilizan para firmar el archivo XML llamado loginTicketResponse.xml (TA), el cual devuelve un token de acceso al WSFE (Web Service Facturación Electrónica).  
Una vez obtenidos los archivos necesarios, se pueden colocar en las siguientes carpetas dependiendo de la infraestructura:
- ```host_certs/``` para Docker.
- ```service/app_certs``` para usar el servicio sin Docker.

### Quick start con Docker

1. Clonar el repositorio
  ```bash
  git clone https://github.com/NehuenLian/AFRelay
  ```
2. Ir al repositorio
  ```bash
  cd AFRelay
  ```
3. Levantar el contenedor
  ```bash
  docker compose up
  ```
4. Health Check readiness:
  ```bash
  curl -i http://localhost:8000/health/readiness
  ```
5. Ver docs de OpenAPI
  ```bash
  http://localhost:8000/docs
  ```

---

### Quick start sin Docker

1. Clonar el repositorio
  ```bash
  git clone https://github.com/NehuenLian/AFRelay
  ```
2. Ir al repositorio
  ```bash
  cd AFRelay
  ```
3. Instalar dependencias
  ```bash
  pip install -r requirements-dev.txt
  ```
4. Levantar FastAPI
  ```bash
  uvicorn service.api.app:app --reload
  ```
5. Health Check liveness:
  ```bash
  curl -i http://127.0.0.1:8000/health/liveness
  ```
6. Health Check readiness:
  ```bash
  curl -i http://127.0.0.1:8000/health/readiness
  ```
7. Ver docs de OpenAPI
  ```bash
  http://127.0.0.1:8000/docs
  ```

### Correr tests y ver coverage

- Todos los tests:
  ```bash
  pytest -v --cov
  ```

- Unit tests:
  ```bash
  pytest tests/unit -v --cov
  ```

- Integration tests:
  ```bash
  pytest tests/integration -v --cov
  ```

## Consideraciones adicionales

- **Persistencia de tickets de acceso:**  
  Si el contenedor o servidor donde se despliega el servicio se cae, no hay problema con los tickets de acceso (`loginTicketResponse.xml`). Al reiniciarse y recibir una solicitud de facturación, el servicio detectará que no existen los archivos y generará un nuevo ticket automáticamente.

- **Despliegue flexible:**  
  No es obligatorio usar Docker. El servicio puede ejecutarse directamente o dentro de cualquier entorno Python, siempre que se respeten los formatos de los archivos de entrada y salida. La protección de las credenciales (tokens, certificados) es responsabilidad del usuario o administrador del entorno.

### Arquitectura

  ```text
  AFRelay
  ├── config/
  ├── host_certs/
  ├── host_xml/
  ├── service/
  │   ├── api/
  │   ├── app_certs/
  │   ├── controllers/
  │   ├── crypto/
  │   ├── payload_builder/
  │   ├── soap_client/
  │   ├── time/
  │   ├── utils/
  │   └── xml_management/
  ├── tests/
  ├── requirements-dev.txt
  └── requirements.txt
  ```

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE) (licencia permisiva de código abierto).

Estás autorizado para usar, copiar, modificar y distribuir el software libremente, siempre incluyendo el aviso de copyright y sin garantías.

---

Autor del proyecto: Nehuen Lián https://github.com/NehuenLian