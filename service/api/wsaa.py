from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from service.controllers.request_access_token_controller import \
    generate_afip_access_token
from service.utils.jwt_validator import verify_token
from service.utils.logger import logger


class loginCmsResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "success"})

router = APIRouter()

@router.post("/wsaa/loginCms", response_model=loginCmsResponse)
async def renew_access_token(jwt = Depends(verify_token)) -> dict:
    
    logger.info("Received request to generate invoice at /wsfe/invoices")

    response_status = await generate_afip_access_token()

    return response_status