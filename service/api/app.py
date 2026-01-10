import os
import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.exceptions import HTTPException

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
from service.utils.afip_token_scheduler import start_scheduler, stop_scheduler
from service.utils.jwt_validator import verify_token
from service.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(lifespan=lifespan)

@app.post("/wsfe/invoices")
async def generate_invoice(sale_data: RootModel, jwt = Depends(verify_token)) -> dict:
    
    logger.info("Received request to generate invoice at /wsfe/invoices")

    sale_data = sale_data.model_dump()
    invoice_result = await request_invoice_controller(sale_data)

    logger.info("Invoice generation completed successfully")

    return invoice_result


@app.post("/wsfe/invoices/last-authorized")
async def last_authorized(comp_info: InvoiceBase, jwt = Depends(verify_token)) -> dict:

    logger.info("Received request to fetch last authorized invoice at /wsfe/invoices/last-authorized")

    comp_info = comp_info.model_dump()
    last_authorized_info = await get_last_authorized_info(comp_info)

    logger.info("Last authorized invoice retrieved successfully")

    return last_authorized_info


@app.post("/wsfe/invoices/query")
async def consult_invoice(comp_info: InvoiceQueryRequest, jwt = Depends(verify_token)) -> dict:

    logger.info("Received request to query specific invoice at /wsfe/invoices/query")

    comp_info = comp_info.model_dump()
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


# ===================
# === DOCS CONFIG ===
# ===================

security = HTTPBasic()

USERNAME = os.getenv('DOCS_USERNAME')
PASSWORD = os.getenv('DOCS_PASSWORD')

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate" : "Basic"}
        )
    return True

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: bool = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")

@app.get("/openapi.json", include_in_schema=False)
def openapi(credentials: bool = Depends(verify_credentials)):
    return JSONResponse(
        get_openapi(title="My API", version="1.0.0", routes=app.routes)
    )