from fastapi import APIRouter, Depends

from service.api.models.fecae_solicitar import FECAESolicitar
from service.api.models.invoice_query import (FECAEAConsultar, FECompConsultar,
                                              FECompUltimoAutorizado)
from service.payload_builder.builder import (add_auth_to_payload, build_auth,
                                             build_fecomp_req)
from service.soap_client.async_client import WSFEClientManager
from service.soap_client.wsdl.wsdl_manager import get_wsfe_wsdl
from service.soap_client.wsfe import consult_afip_wsfe
from service.utils.jwt_validator import verify_token
from service.utils.logger import logger
from service.xml_management.xml_builder import extract_token_and_sign_from_xml

router = APIRouter()
afip_wsdl = get_wsfe_wsdl()


@router.post("/wsfe/FECAEAConsultar")
async def fecaea_consultar(data: FECAEAConsultar, jwt = Depends(verify_token)) -> dict:

    data = data.model_dump()
    auth = build_auth(data)

    async def make_request():
        manager = WSFEClientManager(afip_wsdl)
        client = manager.get_client()
        return await client.service.FECAEAConsultar(auth, data["Periodo"], data["Orden"])
    
    result = await consult_afip_wsfe(make_request, "FECAEAConsultar")
    return result


@router.post("/wsfe/FECAESolicitar")
async def fecae_solicitar(sale_data: FECAESolicitar, jwt = Depends(verify_token)) -> dict:
    
    logger.info("Received request to generate invoice at /wsfe/FECAESolicitar")

    sale_data = sale_data.model_dump()
    token, sign = extract_token_and_sign_from_xml()
    invoice_with_auth = add_auth_to_payload(sale_data, token, sign)

    async def make_request():
        manager = WSFEClientManager(afip_wsdl)
        client = manager.get_client()
        return await client.service.FECAESolicitar(invoice_with_auth['Auth'], invoice_with_auth['FeCAEReq'])

    invoice_result = await consult_afip_wsfe(make_request, "FECAESolicitar")
    return invoice_result


@router.post("/wsfe/FECompUltimoAutorizado")
async def fe_comp_ultimo_autorizado(sale_data: FECompUltimoAutorizado, jwt = Depends(verify_token)) -> dict:
    logger.info("Received request to generate invoice at /wsfe/FECompUltimoAutorizado")

    sale_data = sale_data.model_dump()
    ptovta = sale_data["PtoVta"]
    cbtetipo = sale_data["CbteTipo"]

    auth = build_auth(sale_data)

    async def make_request():
        manager = WSFEClientManager(afip_wsdl)
        client = manager.get_client()
        return await client.service.FECompUltimoAutorizado(auth, ptovta, cbtetipo)

    last_authorized_info = await consult_afip_wsfe(make_request, "FECompUltimoAutorizado")
    return last_authorized_info


@router.post("/wsfe/FECompConsultar")
async def fe_comp_consultar(comp_info: FECompConsultar, jwt = Depends(verify_token)) -> dict:
    logger.info("Received request to query specific invoice at /wsfe/FECompConsultar")

    comp_info = comp_info.model_dump()
    fecomp_req = build_fecomp_req(comp_info)

    auth = build_auth(comp_info)

    async def make_request():
        manager = WSFEClientManager(afip_wsdl)
        client = manager.get_client()
        return await client.service.FECompConsultar(auth, fecomp_req)

    result = await consult_afip_wsfe(make_request, "FECompConsultar")
    return result