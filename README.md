<p align="center">
  <a href="https://codecov.io/github/NehuenLian/AFRelay">
    <img src="https://codecov.io/github/NehuenLian/AFRelay/graph/badge.svg?token=20WL0URAGI" alt="codecov"/>
  </a>
</p>
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

# AFRelay: Billing Microservice with Integration to the Argentine Tax Agency

**AFRelay** is a middleware that eliminates the need to manually build XML and lets developers work with AFIP as if it were a REST API.  
Free. No SaaS. No closed-source infrastructure. No XML and no SOAP manipulated by the developer.

- Fully async I/O network, capable of handling simultaneous requests without blocking.
- Automatically renews the access ticket each 11 hours and when the service starts.
- Does not automatically handle errors or raise exceptions, only returns information as JSON.

### Requirements

To use this service, you need a fiscal key and the corresponding certificates to authenticate with AFIP/ARCA web services.  
The steps to obtain the certificates are available on the official website:
https://www.arca.gob.ar/ws/documentacion/certificados.asp

Once authenticated, the authentication web service will provide two credentials:

- A private key with the extension "```.key```"
- An X.509 certificate with the extension "```.pem```"

This API requires `openssl` to be installed on the system, as it is used to sign CMS requests.  
If running the service without Docker, you need to install the tool:

- **On Debian/Ubuntu:**
  ```bash
  apt-get update && apt-get install -y openssl
  ```

- **On Windows:**
  - Ensure OpenSSL is installed and added to the PATH, for example: ```C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe```.
  - To download OpenSSL: https://slproweb.com/products/Win32OpenSSL.html

### Quick start with Docker

1. Clone the repository
  ```bash
  git clone https://github.com/NehuenLian/AFRelay
  ```
2. Go to repository
  ```bash
  cd AFRelay
  ```
3. Start the container
  ```bash
  docker compose up
  ```
4. Health Check readiness:
  ```bash
  curl -i http://localhost:8000/health/readiness
  ```
5. See OpenAPI docs
  ```bash
  http://localhost:8000/docs
  ```

---

### Quick start without Docker

1. Clone the repository
  ```bash
  git clone https://github.com/NehuenLian/AFRelay
  ```
2. Go to repository
  ```bash
  cd AFRelay
  ```
3. Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
4. Startup FastAPI
  ```bash
  uvicorn service.api.app:app --reload
  ```
5. Health Check readiness:
  ```bash
  curl -i http://127.0.0.1:8000/health/readiness
  ```
6. See OpenAPI docs
  ```bash
  http://localhost:8000/docs
  ```

### Run tests and see coverage

- Full tests:
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

### Additional Considerations

- **Access ticket persistence:**
  If the container or server where the service is deployed goes down, there is no problem with access tickets (`loginTicketResponse.xml`). On restart, if a TA (Access Ticket) comes in and the files are missing, the service will detect it and automatically generate a new ticket.

- **Flexible deployment:**
  Using Docker is optional. The service can run directly or inside any Python environment, as long as input and output file formats are respected. Protecting credentials (tokens, certificates) is the responsibility of the user or system administrator.

### Architecture

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
  └── requirements.txt
  ```

## License

This project is licensed under the [MIT](./LICENSE) license (a permissive open-source license).

You are free to use, copy, modify, and distribute the software, always including the copyright notice and without any warranties.

---

Author: Nehuen Lián https://github.com/NehuenLian