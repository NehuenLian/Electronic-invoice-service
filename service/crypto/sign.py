import base64
import subprocess

from service.utils.logger import logger


def sign_login_ticket_request() -> None:
    logger.debug("Signing loginTicketRequest.xml...")
    # NOTE: Production and Docker environments use Linux.
    # Windows command is kept for local development only.

    # OpenSSL command for windows (ensure you have OpenSSL binaries installed)
    openssl_path = "C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe" # example path
    windows_sign_command = [
        openssl_path, "cms", "-sign",
        "-in", "service/xml_management/xml_files/loginTicketRequest.xml",
        "-out", "service/crypto/loginTicketRequest.xml.cms",
        "-signer", "service/certificates/returned_certificate.pem",
        "-inkey", "service/certificates/PrivateKey.key",
        "-nodetach",
        "-outform", "DER"
    ]

    # Linux/Docker environments
    linux_sign_command = [ 
        "openssl", "cms", "-sign",
        "-in", "service/xml_management/xml_files/loginTicketRequest.xml",
        "-out", "service/crypto/loginTicketRequest.xml.cms",
        "-signer", "service/certificates/returned_certificate.pem",
        "-inkey", "service/certificates/PrivateKey.key",
        "-nodetach",
        "-outform", "DER"
    ]
    
    result_cms = subprocess.run(linux_sign_command, capture_output=True, text=True)
    
    if result_cms.returncode != 0:
        logger.error(f"Error signing CMS: {result_cms.stderr}")
        raise Exception("CMS signing failed.")
    else:
        logger.debug("loginTicketRequest.xml successfully signed.")

def get_binary_cms() -> str:
    with open("service/crypto/LoginTicketRequest.xml.cms", 'rb') as cms:
        cleaned_cms = cms.read()

    b64_cms = base64.b64encode(cleaned_cms).decode("ascii")

    return b64_cms
