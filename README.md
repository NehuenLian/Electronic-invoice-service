![human-coded](https://badgen.net/static/Human%20Coded/100%25/green)[![codecov](https://codecov.io/github/NehuenLian/AFIP-API-middleware/graph/badge.svg?token=20WL0URAGI)](https://codecov.io/github/NehuenLian/AFIP-API-middleware)
# SOAP Web Invoicing Service for Point of Sale with Integration to the Argentine Tax Agency

This system is a web service that acts as middleware between local a system and AFIP (Administración Federal de Ingresos Públicos) / ARCA (Customs Revenue and Control Agency), the tax authority in Argentina. **A middleware that eliminates the need to manually build XML and lets developers work with AFIP as if it were a REST API.** It receives invoices in JSON format, transforms them into XML compatible with AFIP/ARCA Web Services, sends the request via HTTP, processes the response, and returns the result to the POS in JSON format. The goal is to simplify tax compliance.

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

## Main Dependencies:

- **lxml:** Library for XML processing, used to manipulate and validate the XML files required by AFIP/ARCA.  
- **zeep:** SOAP client for easily consuming AFIP/ARCA web services.  
- **fastapi:** Used to build the REST API that receives JSON requests from the POS system.  
- **pydantic:** Data validation and serialization to ensure that the JSONs comply with the schemas.  
- **tenacity:** One of the goals of this service is to generate invoices in as many cases as possible. In the case of non-critical errors, automatic retries are performed using `tenacity`.
- **ntplib:** Used to ensure that the access ticket request contains the time synchronized with AFIP/ARCA.

This API requires `openssl` to be installed on the system, as it is used to sign CMS requests. 

- **On Debian/Ubuntu:**
  ```bash
  apt-get update && apt-get install -y openssl
  ```
- **On Windows:**
  Make sure OpenSSL is installed and the path to openssl.exe is set correctly. 
  You can download OpenSSL here: https://openssl-library.org/source/.

## Stateless?

The service does not store transactional or state information between requests, only the access ticket which persists in memory for 12 hours (until it needs to be refreshed) and is reused for all invoices issued within that period.

## Project Architecture and Structure

The architecture is designed to be simple and easy to understand: one folder per responsibility.  
Below is an ASCII map of the folder structure and a brief description of each one's responsibility:

## Project Structure

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

## Architecture and Directory Description

### `host_certs/`
Host folder containing certificates, private keys, and other cryptographic files.  
These files are mounted into the container as a volume at `app_certs/`.  

### `host_xml/`
Host folder containing the XML files required to send information to AFIP.  
These files are mounted into the container as a volume at `app_xml_files/`.  

### `api/`
Contains the POST endpoint that receives the JSON with sales and invoice information to be built before sending it for approval. It also contains the Pydantic schemas for JSON validation.

### `app_certs/`
Stores certificates, private keys, CSRs, and other cryptographic elements needed to sign the access ticket request.

### `controllers/`
Contains controllers separated by SOAP method. Each controller handles a specific method.

### `crypto/`
Contains the module that signs the access ticket request using the elements from the `app_certs` folder.

### `payload_builder/`
Contains the module that builds and manipulates the dictionaries (`dict`) required by the Zeep library to consume SOAP services.

### `soap_client/`
Handles communication with AFIP/ARCA SOAP services and parses the responses looking for errors. Contains the `.wsdl` files for WSAA and WSFE services.

### `time/`
Contains helper functions for date and time management.

### `utils/`
Contains general helper functions: logger, existence validation, among others.

### `xml_management/`
Stores the XML files required for the service to function and contains all necessary functions to build and manipulate these files.

## Workflow (Simplified)

1. When an invoice is received for authorization:
   - The controller receives the request and sends it directly to AFIP.
   - The response from AFIP is wrapped in a dictionary with the key `status`:
     - `"success"` if the communication with AFIP was successful.
     - `"error"` if there was a communication problem.
   - Errors in the returned XML are not processed or validated.

2. Return the response to the source that submitted the invoice.

## Running Locally Without Docker

1. Clone the repository  
2. Install dependencies: `pip install -r requirements.txt`  
3. Start the service with Uvicorn:  
   - `uvicorn service.api.app:app --reload`  
4. Once the service is running, it will accept a JSON with the structures defined in `api/models/` at the endpoint located in `api/app.py`.

## Example of the JSON Expected by the Endpoint

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

## Explanation of the SOAP services to be queried in this software (the function names are the same as the consulted service)
Directory: `service/soap_client/wsaa.py`

The file `wsaa.py` contains the query to the SOAP method "loginCms" of AFIP/ARCA to authenticate with the tax authority:

- `login_cms(b64ms)`  
  Method that allows obtaining the Access Ticket (TA) to authenticate with AFIP/ARCA.  
  Receives as a parameter a CMS (`b64ms`) that must be in binary format (see `crypto/sign.py/get_binary_cms()`).  
  Returns an XML file called `loginTicketResponse.xml` which contains the token needed to query the other services, expires in 12 hours.

Directory: `service/soap_client/wsfe.py`  
The file `wsfe.py` contains the queries to the SOAP methods of AFIP/ARCA to fetch data about invoices or to authorize electronic receipts:

- `fecae_solicitar(full_built_invoice)`  
  Method that sends the authorization request to issue an electronic receipt (invoice).  
  Receives a `dict` (explained later) with the invoice data, access token, and signature. Returns a CAE (Electronic Authorization Code) as an `OrderedDict` if the invoice is approved, or, if there was an error with the submitted data, also returns an `OrderedDict` with an array appended at the end containing the error information.

- `fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)`  
  This method queries the last authorized receipt by AFIP/ARCA for a specific point of sale (`ptovta`) and receipt type (`cbtetipo`).  
  It is essential to know the next invoice’s sequential number.  
  Receives as arguments:
  
  - `auth`: A `dict` containing the credentials required for authentication, including:
    - `token`: Current access token.
    - `sign`: Digital signature.
    - `cuit`: CUIT of the issuing company.

- `fe_comp_consultar(auth, fecomp_req)`  
  This method queries a specific already issued receipt to obtain information about it.  
  Receives as arguments:
  - `auth`: A `dict` containing the credentials required for authentication, including:
    - `token`: Current access token.
    - `sign`: Digital signature.
    - `cuit`: CUIT of the issuing company.

  - `fecomp_req`: Another `dict` carrying the information needed to identify the receipt to fetch:
    - `PtoVta`: Point of sale from which that receipt was authorized.
    - `CbteTipo`: Receipt type.
    - `CbteNro`: Receipt number. This corresponds to the "CbteDesde" or "CbteHasta" field in the invoices.

---

## Additional Considerations

- **Access Ticket Persistence:**  
  If the container or server where the service is deployed goes down, there is no issue with the access tickets (`loginTicketResponse.xml`). Upon restarting and receiving an invoicing request, the service will detect that the files are missing and automatically generate a new ticket.

- **Flexible Deployment:**  
  Using Docker is not mandatory. The service can run directly as a script or within any Python environment, as long as the input and output file formats are respected. The protection of credentials (tokens, certificates) is the responsibility of the user or environment administrator.

### Full Lifecycle Flow Represented with Logs

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
        <token>P...g==</token>
        <sign>N...o=</sign>
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

### Example of the structure expected by the `/wsfe/invoices` endpoint:

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

### Example of a successful response:

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

### Example of an error response:

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

## License

This project is licensed under the [MIT](./LICENSE) license (a permissive open-source license).

You are free to use, copy, modify, and distribute the software, always including the copyright notice and without any warranties.

---
