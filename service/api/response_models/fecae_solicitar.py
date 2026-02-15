from pydantic import BaseModel, ConfigDict, Field

from service.api.response_models.common import Errors, Events


class Observaciones(BaseModel):
    Code: int
    Msg: str 

class Obs(BaseModel):
    Observaciones: list[Observaciones]

class FECAEDetResponse(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    Concepto: int
    DocTipo: int
    DocNro: int
    CbteDesde: int
    CbteHasta: int
    Resultado: str
    CAE: str | None = None
    CAEFchVto: str | None = None

    obs: Obs | None = Field(None, alias="Obs")

class FeDetResp(BaseModel):
    FECAEDetResponse: list[FECAEDetResponse]

class FeCabResp(BaseModel):
    Cuit: int
    PtoVta: int
    CbteTipo: int
    FchProceso: str
    CantReg: int
    Resultado: str
    Reproceso: str | None = None

class FECAESolicitarResult(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    fe_cab_resp: FeCabResp | None = Field(None, alias="FeCabResp")
    fe_det_resp: FeDetResp | None = Field(None, alias="FeDetResp")

    events: Events | None = Field(None, alias="Events")
    errors: Errors | None = Field(None, alias="Errors")

class FECAESolicitarResponse(BaseModel):
    status: str
    response: FECAESolicitarResult