import pytest
from httpx import AsyncClient

SOAP_RESPONSE = """
<soap-env:Envelope
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ar="http://ar.gov.afip.dif.FEV1/">
    <soap-env:Header/>
    <soap-env:Body>
        <ar:FECAESolicitarResponse>
            <ar:FECAESolicitarResult>
                <ar:FeCabResp>
                    <ar:Cuit>30740253022</ar:Cuit>
                    <ar:PtoVta>1</ar:PtoVta>
                    <ar:CbteTipo>6</ar:CbteTipo>
                    <ar:FchProceso>20251226123045</ar:FchProceso>
                    <ar:CantReg>1</ar:CantReg>
                    <ar:Resultado>A</ar:Resultado>
                    <ar:Reproceso/>
                </ar:FeCabResp>
                <ar:Events>
                    <ar:Evt>
                        <ar:Code>1</ar:Code>
                        <ar:Msg>Evento de prueba</ar:Msg>
                    </ar:Evt>
                </ar:Events>
                <ar:Errors/>
            </ar:FECAESolicitarResult>
        </ar:FECAESolicitarResponse>
    </soap-env:Body>
</soap-env:Envelope>
"""


@pytest.mark.asyncio
async def test_request_invoice_success(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    wsfe_httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        SOAP_RESPONSE, content_type="text/xml"
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
    resp = await client.post("/wsfe/invoices", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"


# Generic error only for test the API behavior in error cases. Exceptions are already tested in unit tests.
@pytest.mark.asyncio
async def test_request_invoice_error(client: AsyncClient, wsfe_httpserver_fixed_port, wsfe_manager, override_auth):

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
    resp = await client.post("/wsfe/invoices", json=payload)

    assert resp.status_code == 200 # 200 its for FastAPI endpoint
    data = resp.json()
    assert data["status"] == "error"
    assert data["error"]["error_type"] == "HTTP Error"
