
from pydantic import BaseModel, ConfigDict, Field


class Obs(BaseModel):
    Code: int
    Msg: str | None = None

class Observaciones(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    obs: list[Obs] | None = Field(None, alias="Obs")

class Evt(BaseModel):
    Code: int
    Msg: str

class Events(BaseModel):
    Evt: list[Evt]

class Err(BaseModel):
    Code: int
    Msg: str

class Errors(BaseModel):
    Err: list[Err]

class FECAEASinMov(BaseModel):
    CAEA: str | None = None
    FchProceso: str | None = None
    PtoVta: int

class FECAEAGet(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    CAEA: str | None = None
    Periodo: int
    Orden: int        
    FchVigDesde: str | None = None
    FchVigHasta: str | None = None
    FchTopeInf: str | None = None
    FchProceso:  str | None = None
    
    observaciones: Observaciones | None = Field(None, alias="Observaciones")

class FECAEAGetResponse(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    fecaea_get: FECAEAGet | None = Field(None, alias="FECAEAGet")

    events: Events | None = Field(None, alias="Events")
    errors: Errors | None = Field(None, alias="Errors")

######### Infrastructure #########
class ErrorDetails(BaseModel):
    method: str
    error_type: str
    details: str

class APIErrorResponseModel(BaseModel):
    status: str
    error: ErrorDetails
