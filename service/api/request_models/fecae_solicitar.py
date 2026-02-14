from pydantic import BaseModel, ConfigDict, Field

from service.api.models.common import Auth


class Actividad(BaseModel):
    Id: int

class Actividades(BaseModel):
    Actividad: list[Actividad]

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
    Cuit: str | None = None
    CbteFch: str

class CbtesAsoc(BaseModel):
    CbteAsoc : list[CbteAsoc]

class FECAEDetRequest(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

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
    FchServHasta: str | None = None
    FchVtoPago: str | None = None
    MonId: str
    MonCotiz: float | None = 0.0
    CanMisMonExt: str | None = None
    CondicionIVAReceptorId: int

    cbtes_asoc: CbtesAsoc | None = Field(None, alias="CbtesAsoc")
    tributos: Tributos | None = Field(None, alias="Tributos")
    iva: Iva | None = Field(None, alias="Iva")
    opcionales: Opcionales | None = Field(None, alias="Opcionales")
    compradores: Compradores | None = Field(None, alias="Compradores")
    periodo_asoc: PeriodoAsoc | None = Field(None, alias="PeriodoAsoc")
    actividades: Actividades | None = Field(None, alias="Actividades")

class FeDetReq(BaseModel):
    FECAEDetRequest: list[FECAEDetRequest]

class FeCabReq(BaseModel):
    CantReg: int
    PtoVta: int
    CbteTipo: int

class FeCAEReq(BaseModel):
    FeCabReq: FeCabReq
    FeDetReq: FeDetReq

class FECAESolicitar(BaseModel):
    Auth: Auth
    FeCAEReq: FeCAEReq