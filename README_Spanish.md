![human-coded](https://badgen.net/static/Human%20Coded/100%25/green)[![codecov](https://codecov.io/github/NehuenLian/AFIP-API-middleware/graph/badge.svg?token=20WL0URAGI)](https://codecov.io/github/NehuenLian/AFIP-API-middleware)
# Servicio Web SOAP de Facturación para Punto de Venta con Integración a la Agencia Tributaria Argentina

Este sistema es un servicio web que actúa como middleware entre un sistema y AFIP (Administración Federal de Ingresos Públicos) / ARCA (Agencia de Recaudación y Control Aduanero) el organismo fiscal de Argentina. **Es un middleware que evita al desarrollador armar XML y que deja comunicarse con AFIP como si fuera una API REST**. Recibe comprobantes en formato JSON, los transforma a XML compatible con los Web Services de AFIP/ARCA, envía la solicitud vía HTTP, procesa la respuesta y devuelve el resultado al POS en formato JSON. El objetivo es simplificar el cumplimiento fiscal.

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://pypi.org/project/zeep/">
    <img src="https://img.shields.io/badge/zeep-4.3.1-green" alt="zeep">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/fastapi-0.115.12-blueviolet" alt="FastAPI">
  </a>
</p>

## Dependencias principales:

- **lxml:** Biblioteca para el procesamiento de los XML, para manipular y validar los archivos XML requeridos por AFIP/ARCA.  
- **zeep:** Cliente SOAP para consumir los servicios web de AFIP/ARCA de forma sencilla.  
- **fastapi:** Para construir la API REST que recibe las solicitudes JSON desde el sistema POS.  
- **pydantic:** Validación y serialización de datos para que los JSON cumplan con los esquemas.  
- **tenacity:** Una de las ideas de este servicio es que logre generar la factura en la mayor cantidad posible de casos. En caso de errores no críticos, se realizan reintentos automáticos usando `tenacity`.
- **ntplib:** Se utiliza en este caso para que la solicitud de ticket de acceso contenga la hora sincronizada con AFIP/ARCA.

Esta API requiere que `openssl` esté instalado en el sistema, ya que se utiliza para firmar solicitudes CMS.

- **En Debian/Ubuntu:**
  ```bash
  apt-get update && apt-get install -y openssl
  ```

- **En Windows:**
  - Asegurarse de que OpenSSL esté instalado y que la ruta a openssl.exe esté configurada correctamente.
  - Para descargar OpenSSL: https://openssl-library.org/source/.

## ¿Stateless?

El servicio no almacena información transaccional ni de estado entre solicitudes, solo el ticket de acceso que persiste en disco durante 12 horas (hasta que se necesite generar otro) y se reutiliza para todas las facturas emitidas en ese período.

## Arquitectura y Estructura del Proyecto

La arquitectura está pensada para ser sencilla y práctica de entender: una carpeta por responsabilidad.  
A continuación se muestra un mapa ASCII de la arquitectura de carpetas y una breve descripción de la responsabilidad de cada una:

## Estructura del Proyecto

```text
INVOICE_SERVICE  
├── service  
│   ├── api/ 
│   ├── app_certs/
│   ├── controllers/
│   ├── crypto/
│   ├── payload_builder/
│   ├── soap_client/
│   ├── time/
│   ├── utils/
│   └── xml_management/
├── .gitignore  
├── main.py  
├── README_English.md  
├── README.md  
└── requirements.txt
```

## Descripción de la arquitectura y los directorios

### `host_certs/`
Carpeta del host que contiene los certificados, claves privadas y otros archivos criptográficos.  
Estos archivos se montan en el contenedor como volumen en `app_certs/`.  

### `host_xml/`
Carpeta del host que contiene los archivos XML necesarios para enviar información a AFIP.  
Estos archivos se montan en el contenedor como volumen en `app_xml_files/`.  

### `api/`
Contiene el endpoint POST que recibe los JSON con información de la venta y de la factura a construir antes de enviarla para su aprobación. También contiene los esquemas de Pydantic para la validación del JSON.

### `app_certs/`
Contiene los certificados, claves privadas, CSRs y otros elementos criptográficos necesarios para firmar la solicitud del ticket de acceso.

### `controllers/`
Contiene controladores separados por método SOAP. Cada controlador maneja un método específico.

### `crypto/`
Contiene el módulo que firma la solicitud del ticket de acceso utilizando los elementos de la carpeta `app_certs`.

### `payload_builder/`
Contiene el módulo que arma y manipula los diccionarios (`dict`) que necesita la librería Zeep para consumir los servicios SOAP.

### `soap_client/`
Maneja la comunicación con los servicios SOAP de AFIP/ARCA. Contiene los archivos `.wsdl` para los servicios WSAA y WSFEE.

### `time/`
Contiene funciones auxiliares para la gestión de fechas y horas.

### `utils/`
Contiene funciones auxiliares generales: logger, validación de existencias, entre otras.

### `xml_management/`
Almacena los archivos XML necesarios para el funcionamiento del servicio y contiene todas las funciones necesarias para construir y manipular estos archivos.

## Flujo de trabajo (simplificado)

1. Cuando llega una factura para autorizar:
   - El controlador recibe la solicitud y la envía directamente a AFIP.
   - La respuesta de AFIP se envuelve en un diccionario con la clave `status`:
     - `"success"` si la comunicación con AFIP fue exitosa.
     - `"error"` si hubo un problema de comunicación.
   - No se procesan ni se validan errores del XML devuelto.

2. Devolver la respuesta al origen que envió la factura.

## Ejecutar localmente sin Docker

1. Clonar el repositorio 
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Levantar el servicio con Uvicorn:
- `uvicorn service.api.app:app --reload`
4. Una vez disponible el servicio, podrá recibir JSON con las estructuras definida en `api/models/` a los endpoints que se encuentran en `api/app.py`.

## Ejemplo del JSON que espera recibir el endpoint `/wsfe/invoices`

```json
{
    "Auth": {
        "Cuit": 20123456789
    },
    "FeCAEReq": {
        "FeCabReq": {
            "CantReg": 1,
            "PtoVta": 1,
            "CbteTipo": 6
        },
        "FeDetReq": {
            "FECAEDetRequest": {
                "Concepto": 1,
                "DocTipo": 96,
                "DocNro": 12345678,
                "CbteDesde": 1,
                "CbteHasta": 1,
                "CbteFch": "20250705",
                "ImpTotal": 1210.00,
                "ImpTotConc": 0.00,
                "ImpNeto": 1000.00,
                "ImpOpEx": 0.00,
                "ImpTrib": 0.00,
                "ImpIVA": 210.00,
                "MonId": "PES",
                "MonCotiz": 1.00,
                "CondicionIVAReceptorId": 5,
                "Iva": {
                    "AlicIva": {
                        "Id": 5,
                        "BaseImp": 1000.00,
                        "Importe": 210.00
                    }
                }
            }
        }
    }
}
```

## Explicación de los servicios SOAP a consultar que se encuentran en este software (el nombre de las funciones es el mismo que el del servicio consultado)
Directorio: `service/soap_client/wsaa.py`

El archivo `wsaa.py` contiene la consulta al metodo SOAP "loginCms" de AFIP/ARCA para autenticarse ante la autoridad fiscal:

- `login_cms(b64ms)`  
  Método que permite obtener el ticket de acceso (TA) para autenticarse ante AFIP/ARCA.
  Recibe como parámetro un CMS (`b64ms`) que debe estar en binario (ver `crypto/sign.py/get_binary_cms()`).
  Devuelve un XML llamado `loginTicketResponse.xml` que contiene el token necesario para consultar los otros servicios, expira en 12 horas.

Directorio: `service/soap_client/wsfe.py`
El archivo `wsfe.py` contiene las consultas a los metodos SOAP de AFIP/ARCA para consultar datos acerca de facturas, o para autorizar comprobantes:

- `fecae_solicitar(full_built_invoice)`  
  Método que envía la solicitud de autorización para emitir el comprobante electrónico (factura).  
  Recibe un `dict` (se explica más adelante) con los datos de la factura, el token de acceso y la firma. Devuelve un CAE (Código de Autorización Electrónico) en forma de `OrderedDict`. Si la factura es aprobada, o, si hubo un error con los datos enviados, devuelve también un `OrderedDict` pero con un array adjunto al final con información del error.

- `fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)`  
  Este método consulta cuál fue el último comprobante autorizado por AFIP/ARCA para un determinado punto de venta (`ptovta`) y tipo de comprobante (`cbtetipo`).  
  Es fundamental para conocer el número correlativo que debe tener la próxima factura.  
  Recibe como argumento:
  
  - `auth`: Un `dict` que contiene las credenciales necesarias para la autenticación, incluyendo:
    - `token`: Token de acceso vigente.
    - `sign`: Firma digital.
    - `cuit`: CUIT de la empresa emisora.

- `fe_comp_consultar(auth, fecomp_req)`  
  Este método consulta un comprobante en específico ya emitido, para obtener información acerca del mismo.
  Recibe como argumento:
  - `auth`: Un `dict` que contiene las credenciales necesarias para la autenticación, incluyendo:
    - `token`: Token de acceso vigente.
    - `sign`: Firma digital.
    - `cuit`: CUIT de la empresa emisora.

  - `fecomp_req`: Otro - `dict` que lleva información para identificar el comprobante a obtener:
    - `PtoVta` : Punto de venta desde el cual se autorizó ese comprobante.
    - `CbteTipo`: Tipo de comprobante.
    - `CbteNro`: Número de comprobante. Es el campo "CbteDesde" o "CbteHasta" en las facturas. 
---

## Consideraciones adicionales

- **Persistencia de tickets de acceso:**  
  Si el contenedor o servidor donde se despliega el servicio se cae, no hay problema con los tickets de acceso (`loginTicketResponse.xml`). Al reiniciarse y recibir una solicitud de facturación, el servicio detectará que no existen los archivos y generará un nuevo ticket automáticamente.

- **Despliegue flexible:**  
  No es obligatorio usar Docker. El servicio puede ejecutarse directamente como script o dentro de cualquier entorno Python, siempre que se respeten los formatos de los archivos de entrada y salida. La protección de las credenciales (tokens, certificados) es responsabilidad del usuario o administrador del entorno.

### Flujo de vida completo representado con logs

```
2025-08-16 14:49:56,869 - INFO - Starting the invoice request process...
2025-08-16 14:49:56,870 - INFO - Checking if loginTicketResponse exists...
2025-08-16 14:49:56,870 - INFO - loginTicketResponse exists.
2025-08-16 14:49:56,870 - INFO - Checking if the token has expired...
2025-08-16 14:49:56,870 - DEBUG - Running is_expired() function for loginTicketRequest.xml
2025-08-16 14:49:56,870 - DEBUG - Consulting NTP for get the datetime...
2025-08-16 14:49:56,902 - DEBUG - Datetime values: epoch: 1755366573 | gentime: 2025-08-16T17:49:33Z | exptime: 2025-08-16T17:59:33Z
2025-08-16 14:49:56,906 - INFO - The token has expired
2025-08-16 14:49:56,906 - DEBUG - Consulting NTP for get the datetime...
2025-08-16 14:49:56,932 - DEBUG - Datetime values: epoch: 1755366573 | gentime: 2025-08-16T17:49:33Z | exptime: 2025-08-16T17:59:33Z
2025-08-16 14:49:56,933 - INFO - loginTicketRequest.xml successfully saved.
2025-08-16 14:49:56,933 - DEBUG - Signing loginTicketRequest.xml...        
2025-08-16 14:49:56,973 - DEBUG - loginTicketRequest.xml successfully signed.
2025-08-16 14:49:56,973 - INFO - Starting CMS login request to AFIP
2025-08-16 14:49:57,164 - INFO - CMS login request to AFIP ended successfully.
2025-08-16 14:49:57,164 - DEBUG - login_ticket_response: <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<loginTicketResponse version="1.0">
    <header>
        <source>CN=wsaahomo, O=AFIP, C=AR, SERIALNUMBER=CUIT 44352675245</source>
        <destination>SERIALNUMBER=CUIT 20123456789, CN=certificadodefinitivo</destination>
        <uniqueId>365485143</uniqueId>
        <generationTime>2025-08-16T14:49:34.147-03:00</generationTime>
        <expirationTime>2025-08-17T02:49:34.147-03:00</expirationTime>
    </header>
    <credentials>
        <token>PD94bWwgdm...KPC9zc28+Cg==</token>
        <sign>N82Px2...rhpho=</sign>
    </credentials>
</loginTicketResponse>

2025-08-16 14:49:57,166 - INFO - loginTicketResponse.xml successfully saved.
2025-08-16 14:49:57,166 - INFO - Token generated.
2025-08-16 14:49:57,166 - INFO - Generating invoice...
2025-08-16 14:49:57,166 - DEBUG - Auth added to payload.
2025-08-16 14:49:57,166 - INFO - Generating invoice...
2025-08-16 14:49:57,512 - DEBUG - Response: {
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250816144936',
        'CantReg': 1,
        'Resultado': 'R',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 69,
                'CbteHasta': 69,
                'CbteFch': '20250816',
                'Resultado': 'R',
                'Observaciones': None,
                'CAE': None,
                'CAEFchVto': None
            }
        ]
    },
    'Events': None,
    'Errors': None
}
2025-08-16 14:49:58,239 - DEBUG - Zeep object converted to dict.
2025-08-16 14:49:58,239 - INFO - Invoice generated.
```

---

### Ejemplo de la estructura de lo que debe recibir `fecae_solicitar(full_built_invoice)`:

```text
{
  "Auth": {
    "Cuit": 20123456789,
    "Token": "PD94...28+Cg==",
    "Sign": "ikM/Ut...wFwvk="
  },
  "FeCAEReq": {
    "FeCabReq": {
      "CantReg": 1,
      "PtoVta": 1,
      "CbteTipo": 6
    },
    "FeDetReq": {
      "FECAEDetRequest": {
        "Concepto": 1,
        "DocTipo": 96,
        "DocNro": 12345678,
        "CbteDesde": 69,
        "CbteHasta": 69,
        "CbteFch": "20250705",
        "ImpTotal": 1210.0,
        "ImpTotConc": 0.0,
        "ImpNeto": 1000.0,
        "ImpOpEx": 0.0,
        "ImpTrib": 0.0,
        "ImpIVA": 210.0,
        "MonId": "PES",
        "MonCotiz": 1.0,
        "CondicionIVAReceptorId": 5,
        "Iva": {
          "AlicIva": {
            "Id": 5,
            "BaseImp": 1000.0,
            "Importe": 210.0
          }
        }
      }
    }
  }
}
```

### Ejemplo de respuesta exitosa:

```text
{
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250706220036',
        'CantReg': 1,
        'Resultado': 'A',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 76,
                'CbteHasta': 76,
                'CbteFch': '20250705',
                'Resultado': 'A',
                'Observaciones': None,
                'CAE': '75272259316252',
                'CAEFchVto': '20250715'
            }
        ]
    },
    'Events': None,
    'Errors': None
}
```

### Ejemplo de respuesta con error:

```text
{
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250706215928',
        'CantReg': 1,
        'Resultado': 'R',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 69,
                'CbteHasta': 69,
                'CbteFch': '20250705',
                'Resultado': 'R',
                'Observaciones': None,
                'CAE': None,
                'CAEFchVto': None
            }
        ]
    },
    'Events': None,
    'Errors': {
        'Err': [
            {
                'Code': 10016,
                'Msg': 'El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.'
            }
        ]
    }
}
```

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE) (licencia permisiva de código abierto).

Podés usar, copiar, modificar y distribuir el software libremente, siempre incluyendo el aviso de copyright y sin garantías.

---
