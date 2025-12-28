from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from service.api.models.invoice_authorization import RootModel
from service.api.models.invoice_query import InvoiceBase, InvoiceQueryRequest
from service.controllers.consult_invoice_controller import \
    consult_specific_invoice
from service.controllers.readiness_health_controller import \
    readiness_health_check
from service.controllers.request_invoice_controller import \
    request_invoice_controller
from service.controllers.request_last_authorized_controller import \
    get_last_authorized_info
from service.soap_client.async_client import WSFEClientManager
from service.soap_client.wsdl.wsdl_manager import get_wsfe_wsdl
from service.utils.afip_token_scheduler import start_scheduler, stop_scheduler
from service.utils.convert_to_dict import convert_pydantic_model_to_dict
from service.utils.jwt_validator import verify_token
from service.utils.logger import logger

afip_wsdl = get_wsfe_wsdl()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    manager = WSFEClientManager(afip_wsdl)
    yield
    await manager.close()
    stop_scheduler()

app = FastAPI(lifespan=lifespan)

@app.post("/wsfe/invoices")
async def generate_invoice(sale_data: RootModel, jwt = Depends(verify_token)) -> dict:
    
    logger.info("Received request to generate invoice at /wsfe/invoices")

    sale_data = convert_pydantic_model_to_dict(sale_data)
    invoice_result = await request_invoice_controller(sale_data)

    logger.info("Invoice generation completed successfully")

    return invoice_result


@app.post("/wsfe/invoices/last-authorized")
async def last_authorized(comp_info: InvoiceBase, jwt = Depends(verify_token)) -> dict:

    logger.info("Received request to fetch last authorized invoice at /wsfe/invoices/last-authorized")

    comp_info = convert_pydantic_model_to_dict(comp_info)
    last_authorized_info = await get_last_authorized_info(comp_info)

    logger.info("Last authorized invoice retrieved successfully")

    return last_authorized_info


@app.post("/wsfe/invoices/query")
async def consult_invoice(comp_info: InvoiceQueryRequest, jwt = Depends(verify_token)) -> dict:

    logger.info("Received request to query specific invoice at /wsfe/invoices/query")

    comp_info = convert_pydantic_model_to_dict(comp_info)
    result = await consult_specific_invoice(comp_info)

    logger.info("Invoice query completed successfully")

    return result

# ===================
# == HEALTH CHECKS ==
# ===================

@app.get("/health/liveness")
def liveness() -> dict:

    return {"health" : "OK"}

@app.get("/health/readiness")
async def readiness() -> dict:

    status = await readiness_health_check()
    return status
