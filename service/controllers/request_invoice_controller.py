from service.payload_builder.builder import add_auth_to_payload
from service.soap_client.wsfe import fecae_solicitar
from service.utils.logger import logger
from service.xml_management.xml_builder import (
    extract_token_and_sign_from_xml)


async def request_invoice_controller(sale_data: dict) -> dict:

    logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_xml()
    invoice_with_auth = add_auth_to_payload(sale_data, token, sign)
    invoice_result = await fecae_solicitar(invoice_with_auth)

    return invoice_result
