import logging
from builtins import ConnectionResetError

from requests.exceptions import (  # Zeep uses requests behind it.
    ConnectionError, Timeout)
from tenacity import (before_sleep_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_fixed)
from zeep import Client
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

from service.soap_client.format_error import build_error_response
from service.utils.convert_to_dict import convert_zeep_object_to_dict
from service.utils.logger import logger
from service.soap_client.wsdl.wsdl_manager import get_wsfe_wsdl

afip_wsdl = get_wsfe_wsdl()

# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
def fecae_solicitar(full_built_invoice: dict) -> dict:

    logger.info(f"Generating invoice...")
    METHOD = "FECAESolicitar"

    try:
        client = Client(wsdl=afip_wsdl)
        invoice_result = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])
        
        logger.debug(f"Response: {invoice_result}")
        invoice_result = convert_zeep_object_to_dict(invoice_result)
        return {
                "status" : "success",
                "response" : invoice_result
                }
    
    except (ConnectionError, Timeout):
        return build_error_response(METHOD, "Network error", str(e))
    
    except TransportError as e:
        return build_error_response(METHOD, "HTTP Error", str(e))

    except Fault as e:
        # SOAP Faults indicate that the request could not be processed by the service, 
        # often due to invalid input, datatype mismatches, or business rule violations. 
        # These errors are the caller's responsibility to handle.
        
        logger.debug(f"SOAP FAULT in fecae_solicitar: {e}")
        return build_error_response(METHOD, "SoapFault", str(e))
    
    except XMLSyntaxError as e:
        return build_error_response(METHOD, "Invalid AFIP response", str(e))

    except Exception as e:
        logger.error(f"General exception in fecae_solicitar: {e}")
        return build_error_response(METHOD, "unknown", str(e))


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
def fe_comp_ultimo_autorizado(auth: dict, ptovta: int, cbtetipo: int) -> dict:
    
    logger.info(f"Consulting last authorized invoice...")
    METHOD = "FECompUltimoAutorizado"

    try:
        client = Client(wsdl=afip_wsdl)
        last_authorized_invoice = client.service.FECompUltimoAutorizado(auth, ptovta, cbtetipo)
        logger.debug(f"Response: {last_authorized_invoice}")

        last_authorized_invoice = convert_zeep_object_to_dict(last_authorized_invoice)
        return {
                "status" : "success",
                "response" : last_authorized_invoice
                }
    
    except (ConnectionError, Timeout):
        return build_error_response(METHOD, "Network error", str(e))
    
    except TransportError as e:
        return build_error_response(METHOD, "HTTP Error", str(e))

    except Fault as e:
        # SOAP Faults indicate that the request could not be processed by the service, 
        # often due to invalid input, datatype mismatches, or business rule violations. 
        # These errors are the caller's responsibility to handle.
        
        logger.debug(f"SOAP FAULT in fe_comp_ultimo_autorizado: {e}")
        return build_error_response(METHOD, "SoapFault", str(e))
    
    except XMLSyntaxError as e:
        return build_error_response(METHOD, "Invalid AFIP response", str(e))

    except Exception as e:
        logger.error(f"General exception in fe_comp_ultimo_autorizado: {e}")
        return build_error_response(METHOD, "unknown", str(e))
    

# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
def fe_comp_consultar(auth: dict, 
                    cbtetipo: int, 
                    cbtenro: int, 
                    ptovta: int) -> dict:
        
    logger.info(f"Consulting last authorized invoice...")
    METHOD = "FECompConsultar"

    fecomp_req = {
        'CbteTipo': cbtetipo,
        'CbteNro': cbtenro,
        'PtoVta': ptovta
    }

    try:
        client = Client(wsdl=afip_wsdl)
        invoice_info = client.service.FECompConsultar(auth, fecomp_req)
        logger.debug(f"Response: {invoice_info}")

        invoice_info = convert_zeep_object_to_dict(invoice_info)
        return {
                "status" : "success",
                "response" : invoice_info
                }
    
    except (ConnectionError, Timeout):
        return build_error_response(METHOD, "Network error", str(e))
    
    except TransportError as e:
        return build_error_response(METHOD, "HTTP Error", str(e))

    except Fault as e:
        # SOAP Faults indicate that the request could not be processed by the service, 
        # often due to invalid input, datatype mismatches, or business rule violations. 
        # These errors are the caller's responsibility to handle.
        
        logger.debug(f"SOAP FAULT in fe_comp_consultar: {e}")
        return build_error_response(METHOD, "SoapFault", str(e))
    
    except XMLSyntaxError as e:
        return build_error_response(METHOD, "Invalid AFIP response", str(e))

    except Exception as e:
        logger.error(f"General exception in fe_comp_consultar: {e}")
        return build_error_response(METHOD, "unknown", str(e))


# ===================
# == HEALTH CHECK ===
# ===================

def wsfe_dummy():
    """
    WSFE health cheack
    """
    logger.info(f"Consulting WSFE dummy method (health check)...")
    afip_wsdl = get_wsfe_wsdl()

    try:
        client = Client(wsdl=afip_wsdl)
        health_info = client.service.FEDummy()

        return health_info

    except Exception as e:
        logger.error(f"General exception in wsfe_dummy: {e}")
        return health_info