import pytest
from httpx import AsyncClient

from .soap_responses import FeCompUltimoAutorizadoResponse


@pytest.mark.asyncio
async def test_fe_comp_ultimo_autorizado_success(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    wsfe_httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        FeCompUltimoAutorizadoResponse, content_type="text/xml"
    )

    # Payload
    payload = {
        "Auth": {
            "Cuit": 30740253022
        },
        "PtoVta": 1,
        "CbteTipo": 6
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/FECompUltimoAutorizado", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"


# Generic error only for test the API behavior in error cases. Exceptions are already tested in unit tests.
@pytest.mark.asyncio
async def test_fe_comp_ultimo_autorizado_error(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

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
        "PtoVta": 1,
        "CbteTipo": 6
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/FECompUltimoAutorizado", json=payload)

    assert resp.status_code == 200 # 200 its for FastAPI endpoint
    data = resp.json()
    assert data["status"] == "error"
    assert data["error"]["error_type"] == "HTTP Error"