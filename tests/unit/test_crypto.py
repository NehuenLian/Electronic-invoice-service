from unittest.mock import patch
from service.crypto.sign import sign_login_ticket_request
import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

def test_sign_login_ticket_request():

    login_ticket_request_bytes, private_key_bytes, certificate_bytes = generate_test_files()
    b64_cms = sign_login_ticket_request(login_ticket_request_bytes, private_key_bytes, certificate_bytes)

    assert len(b64_cms) > 0


# Generate a fake private key, cert and xml
def generate_test_files() -> tuple[bytes, bytes, bytes]:

    # Create private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    # ===

    # Create certificate
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Test City")
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1))
        .sign(private_key, hashes.SHA256())
    )
    cert_bytes_pem = cert.public_bytes(serialization.Encoding.PEM)
    # ===

    # Create XML
    login_ticket_request = """<?xml version='1.0' encoding='UTF-8'?>
    <loginTicketRequest>
    <header>
        <uniqueId>1767764408</uniqueId>
        <generationTime>2026-01-07T05:40:08Z</generationTime>
        <expirationTime>2026-01-07T05:50:08Z</expirationTime>
    </header>
    <service>wsfe</service>
    </loginTicketRequest>
    """
    xml_bytes = login_ticket_request.encode('utf-8')
    # ===

    return xml_bytes, private_key_bytes, cert_bytes_pem
