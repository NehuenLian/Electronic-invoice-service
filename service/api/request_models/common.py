from pydantic import BaseModel


class Auth(BaseModel):
    """
    Token and Sign will taken 
    from loginTicketResponse.xml in the service
    """
    Cuit: int