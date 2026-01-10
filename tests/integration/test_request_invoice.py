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
async def test_request_invoice_minimal(client: AsyncClient, httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        SOAP_RESPONSE, content_type="text/xml"
    )

    # Payload
    payload = {
        "Auth": {"Cuit": 30740253022},
        "FeCAEReq": {
            "FeCabReq": {"CantReg": 1, "PtoVta": 1, "CbteTipo": 6},
            "FeDetReq": {
                "FECAEDetRequest": {
                    "Concepto": 1,
                    "DocTipo": 96,
                    "DocNro": 12345678,
                    "CbteDesde": 101,
                    "CbteHasta": 101,
                    "CbteFch": "20251226",
                    "ImpTotal": 1210.0,
                    "ImpTotConc": 0.0,
                    "ImpNeto": 1000.0,
                    "ImpOpEx": 0.0,
                    "ImpTrib": 0.0,
                    "ImpIVA": 210.0,
                    "MonId": "PES",
                    "MonCotiz": 1.0,
                    "CondicionIVAReceptorId": 5,
                    "Iva": {"AlicIva": {"Id": 5, "BaseImp": 1000.0, "Importe": 210.0}},
                }
            },
        },
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/invoices", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
