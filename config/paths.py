from functools import lru_cache
from pathlib import Path


class AfipPaths:
    """
    Centralizes AFIP file paths using the Path Object pattern.
    Allows injection of different base directories for testing.
    """
    def __init__(self, base_xml: Path, base_crypto: Path, base_certs: Path) -> None:
        self.base_xml = base_xml
        self.base_crypto = base_crypto
        self.base_certs = base_certs

    @property
    def login_request(self) -> Path:
        return self.base_xml / "loginTicketRequest.xml"
    
    @property
    def login_response(self) -> Path:
        return self.base_xml / "loginTicketResponse.xml"
    
    @property
    def login_request_cms(self) -> Path:
        return self.base_crypto / "loginTicketRequest.xml.cms"
    
    @property
    def certificate(self) -> Path:
        return self.base_certs / "returned_certificate.pem"
    
    @property
    def private_key(self) -> Path:
        return self.base_certs / "PrivateKey.key"
    
@lru_cache
def get_afip_paths() -> AfipPaths:
    return AfipPaths(
        base_xml = Path("service/xml_management/app_xml_files"),
        base_crypto = Path("service/crypto"),
        base_certs = Path("service/app_certs"),
    )