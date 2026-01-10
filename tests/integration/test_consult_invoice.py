import pytest
from httpx import AsyncClient

SOAP_RESPONSE = """<?xml version='1.0' encoding='UTF-8'?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <FECompConsultarResponse xmlns="http://ar.gov.afip.dif.FEV1/">
            <FECompConsultarResult>
                <ResultGet>
                
                    <Concepto>1</Concepto>
                    <DocTipo>80</DocTipo>
                    <DocNro>20123456789</DocNro>
                    <CbteDesde>100</CbteDesde>
                    <CbteHasta>100</CbteHasta>
                    <CbteFch>20260109</CbteFch>
                    <ImpTotal>100.00</ImpTotal>
                    <ImpTotConc>0.00</ImpTotConc>
                    <ImpNeto>100.00</ImpNeto>
                    <ImpOpEx>0.00</ImpOpEx>
                    <ImpTrib>0.00</ImpTrib>
                    <ImpIVA>21.00</ImpIVA>
                    <MonId>PES</MonId>
                    <MonCotiz>1.000</MonCotiz>

                    <PtoVta>1</PtoVta>
                    <CbteTipo>6</CbteTipo>
                </ResultGet>
                <Errors/>
                <Events/>
            </FECompConsultarResult>
        </FECompConsultarResponse>
    </soap:Body>
</soap:Envelope>
"""


@pytest.mark.asyncio
async def test_consult_invoice_minimal(client: AsyncClient, httpserver_fixed_port, wsfe_manager, override_auth):

    # Configure http server
    httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        SOAP_RESPONSE, content_type="text/xml"
    )

    # Payload
    payload = {
        "Cuit": 30740253022,
        "PtoVta": 1,
        "CbteTipo": 6,
        "CbteNro": 100,
    }

    # Fastapi endpoint call
    resp = await client.post("/wsfe/invoices/query", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"