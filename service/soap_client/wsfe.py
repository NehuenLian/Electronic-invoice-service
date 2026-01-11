import logging
from builtins import ConnectionResetError

import httpx
from tenacity import (before_sleep_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_fixed)
from zeep.exceptions import Fault, TransportError, XMLSyntaxError
from zeep.helpers import serialize_object

from service.soap_client.async_client import WSFEClientManager
from service.soap_client.format_error import build_error_response
from service.soap_client.wsdl.wsdl_manager import get_wsfe_wsdl
from service.utils.logger import logger


@retry(
        retry=retry_if_exception_type(( ConnectionResetError, httpx.ConnectError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
async def consult_afip_wsfe(make_request, METHOD: str) -> dict:
        
    try:
        afip_response = await make_request()
        logger.debug(f"Response: {afip_response}")

        # Zeep returns an object of type '<class 'zeep.objects.[service response]'>'.
        # To work with the returned data, this object needs to be converted into a dictionary using serialize_object().
        afip_response = serialize_object(afip_response)

        return {
                "status" : "success",
                "response" : afip_response
                }
    
    except (httpx.ConnectError, httpx.TimeoutException) as e:
        return build_error_response(METHOD, "Network error", str(e))
    
    except TransportError as e:
        return build_error_response(METHOD, "HTTP Error", str(e))

    except Fault as e:
        # SOAP Faults here are not caused by user input.
        # Zeep owns the XML generation, so any structural or datatype issue leading to a
        # SOAP Fault originates from Zeep or the remote service, not from this layer.
        
        logger.debug(f"SOAP FAULT in {METHOD}: {e}")
        return build_error_response(METHOD, "SOAPFault", str(e))
    
    except XMLSyntaxError as e:
        return build_error_response(METHOD, "Invalid AFIP response", str(e))

    except Exception as e:
        logger.error(f"General exception in {METHOD}: {e}")
        return build_error_response(METHOD, "unknown", str(e))


# ===================
# == HEALTH CHECK ===
# ===================

afip_wsdl = get_wsfe_wsdl()

async def wsfe_dummy():
    """
    WSFE health cheack
    """
    logger.info(f"Consulting WSFE dummy method (health check)...")
    manager = WSFEClientManager(afip_wsdl)
    client = manager.get_client()
    try:
        health_info = await client.service.FEDummy()
        return health_info

    except Exception as e:
        logger.error(f"General exception in wsfe_dummy: {e}")
        return health_info