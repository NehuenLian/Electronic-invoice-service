from service.payload_builder.builder import add_auth_to_payload, build_auth, build_fecomp_req
from unittest.mock import patch

def test_add_auth_to_payload():

    fake_sale_data = { "Auth": {} }
    fake_token = "fake_token"
    fake_sign = "fake_sign"

    fake_sale_data_with_auth = add_auth_to_payload(fake_sale_data, "fake_token", "fake_sign")

    assert fake_sale_data_with_auth['Auth']['Token'] == fake_token
    assert fake_sale_data_with_auth['Auth']['Sign'] == fake_sign


def test_build_fecomp_req():

    def fake_extract_token_and_sign_from_xml() -> tuple[str, str]:
        return "fake_token", "fake_sign"
    
    sale_data = {
            "Cuit" : 30740253022
            }   

    with patch("service.xml_management.xml_builder.extract_token_and_sign_from_xml", fake_extract_token_and_sign_from_xml):
        auth = build_auth(sale_data)

    assert auth["Token"] == "fake_token"
    assert auth["Sign"] == "fake_sign"
    assert auth["Cuit"] == 30740253022


def test_build_fecomp_req():
    """
    class InvoiceBase(BaseModel):
        Cuit: int
        PtoVta: int
        CbteTipo: int
    """

    comp_info = {
            "PtoVta" : 1,
            "CbteTipo" : 1,
            "CbteNro" : 1
            }

    fecomp_req = build_fecomp_req(comp_info)

    assert fecomp_req["PtoVta"] == 1
    assert fecomp_req["CbteTipo"] == 1
    assert fecomp_req["CbteNro"] == 1