import httpx
from zeep import AsyncClient
from zeep.transports import AsyncTransport

from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.soap_client.wsaa import consult_afip_wsaa
from service.soap_client.wsdl.wsdl_manager import get_wsaa_wsdl
from service.time.time_management import generate_ntp_timestamp
from service.utils.logger import logger
from service.xml_management.xml_builder import (
    build_login_ticket_request, parse_and_save_loginticketresponse, save_xml)

afip_wsdl = get_wsaa_wsdl()

async def generate_afip_access_token() -> dict:

    logger.info("Generating a new access token...")

    root = build_login_ticket_request(generate_ntp_timestamp)
    save_xml(root, "loginTicketRequest.xml")
    sign_login_ticket_request()
    b64_cms = get_binary_cms()

    async def login_cms():
        try:
            httpx_client = httpx.AsyncClient(timeout=30.0)
            transport = AsyncTransport(client=httpx_client)
            client = AsyncClient(wsdl=afip_wsdl, transport=transport)
            return await client.service.loginCms(b64_cms)

        finally:
            if client and client.transport:
                await client.transport.aclose()
            else:
                await httpx_client.aclose()

    login_ticket_response = await consult_afip_wsaa(login_cms, "loginCms")

    if login_ticket_response["status"] == "success":
        parse_and_save_loginticketresponse(login_ticket_response["response"], save_xml)
    
        logger.info("Token generated successfully.")
        return {
            "status" : "success"
            }

    else:
        logger.error("Failed to generate access token.")
        return {
            "status" : "error generating access token."
            }
