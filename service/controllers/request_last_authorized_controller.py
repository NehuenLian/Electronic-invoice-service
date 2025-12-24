from service.payload_builder.builder import build_auth
from service.soap_client.wsfe import fe_comp_ultimo_autorizado
from service.utils.logger import logger
from service.xml_management.xml_builder import extract_token_and_sign_from_xml


def get_last_authorized_info(comp_info: dict) -> dict:

    token, sign = extract_token_and_sign_from_xml("loginTicketResponse.xml")

    cuit = comp_info["Cuit"]
    ptovta = comp_info["PtoVta"]
    cbtetipo = comp_info["CbteTipo"]

    auth = build_auth(token, sign, cuit)
    last_authorized_invoice = fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)

    return last_authorized_invoice