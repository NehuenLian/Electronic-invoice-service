from pydantic import BaseModel

from service.api.models.common import Auth


class FeCompConsReq(BaseModel):
    PtoVta: int
    CbteTipo: int
    CbteNro: int

class FECompConsultar(BaseModel):
    Auth: Auth
    FeCompConsReq: FeCompConsReq
