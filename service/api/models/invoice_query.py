from pydantic import BaseModel


class InvoiceBaseQuery(BaseModel):
    Cuit: int

class FECompTotXRequest(InvoiceBaseQuery):
    pass

class FECompUltimoAutorizado(InvoiceBaseQuery):
    PtoVta: int
    CbteTipo: int

class FECompConsultar(InvoiceBaseQuery):
    PtoVta: int
    CbteTipo: int
    CbteNro: int

class FECAEASolicitar(InvoiceBaseQuery):
    Periodo: int
    Orden: int

class FECAEASinMovimientoConsultar(InvoiceBaseQuery):
    CAEA: str
    PtoVta: int

class FECAEASinMovimientoInformar(InvoiceBaseQuery):
    PtoVta: int
    CAEA: str

class FECAEAConsultar(InvoiceBaseQuery):
    Periodo: int
    Orden: int