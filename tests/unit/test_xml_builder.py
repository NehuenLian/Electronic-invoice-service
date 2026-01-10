from unittest.mock import MagicMock

from service.xml_management.xml_builder import (
    build_login_ticket_request, extract_token_and_sign_from_xml, is_expired,
    parse_and_save_loginticketresponse, xml_exists)


def test_build_login_ticket_request():

    def fake_time_provider():
        return (
            1767764408,
            "2026-01-07T05:40:08Z",
            "2026-01-07T05:50:08Z",
        )

    root = build_login_ticket_request(fake_time_provider)

    assert root.find("header/uniqueId").text == "1767764408"

def test_parse_and_save_loginticketresponse():

    loginTicketResponse_mock = """<?xml version='1.0' encoding='UTF-8'?>
    <loginTicketResponse version="1.0">
        <header>
            <source>CN=wsaahomo, O=AFIP, C=AR, SERIALNUMBER=CUIT 33693450239</source>
            <destination>SERIALNUMBER=CUIT 30740253022, CN=certificadodefinitivo</destination>
            <uniqueId>3634574819</uniqueId>
            <generationTime>2026-01-07T02:40:09.235-03:00</generationTime>
            <expirationTime>2026-01-07T14:40:09.235-03:00</expirationTime>
        </header>
        <credentials>
            <token>fake_token</token>
            <sign>fake_sign</sign>
        </credentials>
    <header><source/><destination/><uniqueId/><generationTime/><expirationTime/></header><credentials><token/><sign/></credentials></loginTicketResponse>
    """

    mock_saver = MagicMock()
    parse_and_save_loginticketresponse(loginTicketResponse_mock, mock_saver)

    assert mock_saver.call_count == 1

    root_passed = mock_saver.call_args[0][0]
    assert root_passed.find("header") is not None
    assert root_passed.find("credentials") is not None

def test_extract_token_and_sign_from_xml():

    token, sign = extract_token_and_sign_from_xml()

    assert token == "fake_token"
    assert sign == "fake_sign"

def test_loginTicketRequest_is_expired():

    def fake_time_provider():
        return (
            1767764408,
            "2026-01-07T05:40:08Z",
            "2026-01-07T05:50:08Z",
        )
    
    expired = is_expired("loginTicketRequest.xml", fake_time_provider)
    assert expired == False

def test_loginTicketRequest_exists():

    exists = xml_exists("loginTicketRequest.xml")
    assert exists == True

def test_loginTicketResponse_exists():

    exists = xml_exists("loginTicketResponse.xml")
    assert exists == True