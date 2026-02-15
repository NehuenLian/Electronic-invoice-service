from pydantic import BaseModel, ConfigDict, Field

from service.api.response_models.common import Errors, Events


class Obs(BaseModel):
    Code: int
    Msg: str

class Observaciones(BaseModel):
    Obs: Obs

class PeriodoAsoc(BaseModel):
    FchDesde: str
    FchHasta: str

class Comprador(BaseModel):
    DocTipo: int
    DocNro: int
    Porcentaje: float

class Compradores(BaseModel):
    Comprador: list[Comprador]

class Opcional(BaseModel):
    Id: str
    Valor: str

class Opcionales(BaseModel):
    Opcional: list[Opcional]

class AlicIva(BaseModel):
    Id: int
    BaseImp: float
    Importe: float

class Iva(BaseModel):
    AlicIva: list[AlicIva]

class Tributo(BaseModel):
    Id: int
    Desc: str | None = None
    BaseImp: float
    Alic: float
    Importe: float

class Tributos(BaseModel):
    Tributo: list[Tributo]

class CbteAsoc(BaseModel):
    Tipo: int
    PtoVta: int
    Nro: int

class CbtesAsoc(BaseModel):
    CbteAsoc: CbteAsoc

class ResultGet(BaseModel):
    Concepto: int
    DocTipo: int
    DocNro: int
    CbteDesde: int
    CbteHasta: int
    CbteFch: str
    ImpTotal: float
    ImpTotConc: float
    ImpNeto: float
    ImpOpEx: float
    ImpTrib: float
    ImpIVA: float
    FchServDesde: str | None = None
    FchServHast: str | None = None
    FchVtoPago: str | None = None
    MonId: str
    MonCotiz: float

    cbtes_asoc: CbtesAsoc | None = Field(None, alias="CbtesAsoc")
    tributos: Tributos | None = Field(None, alias="Tributos")
    iva: Iva | None = Field(None, alias="Iva")
    opcionales: Opcionales | None = Field(None, alias="Opcionales")
    compradores: Compradores | None = Field(None, alias="Compradores")
    periodo_asoc: PeriodoAsoc | None = Field(None, alias="PeriodoAsoc")

    Resultado: str
    CodAutorizacion: str
    EmisionTipo: str
    FchVto: str
    FchProceso: str

    observaciones: Observaciones | None = Field(None, alias="Observaciones")

    PtoVta: int
    CbteTipo: int

class FECompConsultaResponse(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    result_get: ResultGet | None = Field(None, alias="ResultGet")

    errors: Errors | None = Field(None, alias="Errors")
    events: Events | None = Field(None, alias="Events")

class FECompConsultarResponse(BaseModel):
    status: str
    response: FECompConsultaResponse