import pytest
from httpx import AsyncClient

from .soap_responses import FECAESolicitarResponse


@pytest.mark.asyncio
async def test_fecae_solicitar_success(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    wsfe_httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        FECAESolicitarResponse, content_type="text/xml"
    )

    payload = {
        "Auth": {
            "Cuit": 30740253022
        },
        "FeCAEReq": {
            "FeCabReq": {
                "CantReg": 1,
                "PtoVta": 1,
                "CbteTipo": 11
            },
            "FeDetReq": {
                "FECAEDetRequest": [
                    {
                        "Concepto": 1,
                        "DocTipo": 99,
                        "DocNro": 0,
                        "CbteDesde": 2,
                        "CbteHasta": 2,
                        "CbteFch" : "20260125",
                        "ImpTotal": 100.0,
                        "ImpNeto": 100.0,
                        "ImpTotConc": 0.0,
                        "ImpOpEx": 0.0,
                        "ImpTrib": 0.0,
                        "ImpIVA": 0.0,
                        "MonId": "PES",
                        "MonCotiz": 1,
                        "CondicionIVAReceptorId": 5,
                    }
                ]
            }
        }
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/FECAESolicitar", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"


# Generic error only for test the API behavior in error cases. Exceptions are already tested in unit tests.
@pytest.mark.asyncio
async def test_fecae_solicitar_error(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    wsfe_httpserver_fixed_port.expect_request("/not_existent", method="POST").respond_with_data(
        "Internal Server Error",
        status=500,
        content_type="text/plain",
    )

    # Payload
    payload = {
        "Auth": {
            "Cuit": 30740253022
        },
        "FeCAEReq": {
            "FeCabReq": {
                "CantReg": 1,
                "PtoVta": 1,
                "CbteTipo": 11
            },
            "FeDetReq": {
                "FECAEDetRequest": [
                    {
                        "Concepto": 1,
                        "DocTipo": 99,
                        "DocNro": 0,
                        "CbteDesde": 2,
                        "CbteHasta": 2,
                        "CbteFch" : "20260125",
                        "ImpTotal": 100.0,
                        "ImpNeto": 100.0,
                        "ImpTotConc": 0.0,
                        "ImpOpEx": 0.0,
                        "ImpTrib": 0.0,
                        "ImpIVA": 0.0,
                        "MonId": "PES",
                        "MonCotiz": 1,
                        "CondicionIVAReceptorId": 5,
                    }
                ]
            }
        }
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/FECAESolicitar", json=payload)

    assert resp.status_code == 200 # 200 its for FastAPI endpoint
    data = resp.json()
    assert data["status"] == "error"
    assert data["error"]["error_type"] == "HTTP Error"
