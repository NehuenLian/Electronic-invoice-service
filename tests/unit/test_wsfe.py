import httpx
import pytest
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

from service.soap_client.wsfe import consult_afip_wsfe


# ===== Success =======
@pytest.mark.asyncio
async def test_consult_afip_wsfe_success():

    async def make_request_fake():
        afip_response = { "invoice" : "approved" }
        return { "status" : "success",
                "response" : afip_response }

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "success"
# ====================


# ===== Errors =======
@pytest.mark.asyncio
async def test_consult_afip_wsfe_connection_error():

    async def make_request_fake():
        raise httpx.ConnectError("Network error")

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "error"
    assert response["error"]["error_type"] == "Network error"


@pytest.mark.asyncio
async def test_consult_afip_wsfe_timeout():

    async def make_request_fake():
        raise httpx.TimeoutException("Network error")

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "error"
    assert response["error"]["error_type"] == "Network error"


@pytest.mark.asyncio
async def test_consult_afip_wsfe_transport_error():

    async def make_request_fake():
        raise TransportError("HTTP Error")

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "error"
    assert response["error"]["error_type"] == "HTTP Error"


@pytest.mark.asyncio
async def test_consult_afip_wsfe_soap_fault():

    async def make_request_fake():
        raise Fault("SOAPFault")

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "error"
    assert response["error"]["error_type"] == "SOAPFault"


@pytest.mark.asyncio
async def test_consult_afip_wsfe_xml_syntax_error():

    async def make_request_fake():
        raise XMLSyntaxError("Invalid AFIP response")

    response = await consult_afip_wsfe(make_request_fake, "TestMethod")

    assert response["status"] == "error"
    assert response["error"]["error_type"] == "Invalid AFIP response"
# ====================