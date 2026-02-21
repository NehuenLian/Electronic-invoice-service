from unittest.mock import MagicMock, patch

import pytest
from zeep import AsyncClient
from .soap_responses import loginCmsResponse


@pytest.mark.asyncio
async def test_generate_afip_access_token_success(
                                                client: AsyncClient, 
                                                wsaa_httpserver_fixed_port, 
                                                patch_request_access_token_dependencies,
                                                wsaa_manager, 
                                                override_auth
                                            ):

    # Configure http server
    wsaa_httpserver_fixed_port.expect_request("/soap", method="POST").respond_with_data(
        loginCmsResponse, content_type="text/xml"
    )

    # Magic mocks patched directly in the test for practicality
    xml_saver_mock = MagicMock()
    parse_and_save_loginticketresponse_mock = MagicMock()
    with patch("service.controllers.request_access_token_controller.save_xml", xml_saver_mock):
        with patch("service.controllers.request_access_token_controller.parse_and_save_loginticketresponse", parse_and_save_loginticketresponse_mock):
                  
            resp = await client.post("/wsaa/loginCms")

    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "success"
    assert xml_saver_mock.call_count == 1
    assert parse_and_save_loginticketresponse_mock.call_count == 1


@pytest.mark.asyncio
async def test_generate_afip_access_token_error(
                                                client: AsyncClient, 
                                                wsaa_httpserver_fixed_port, 
                                                patch_request_access_token_dependencies,
                                                wsaa_manager, 
                                                override_auth
                                            ):

    # Configure http server
    wsaa_httpserver_fixed_port.expect_request("/not_existent", method="POST").respond_with_data(
        "Internal Server Error",
        status=500,
        content_type="text/plain",
    )

    # Magic mocks patched directly in the test for practicality
    xml_saver_mock = MagicMock()
    parse_and_save_loginticketresponse_mock = MagicMock()
    with patch("service.controllers.request_access_token_controller.save_xml", xml_saver_mock):
        with patch("service.controllers.request_access_token_controller.parse_and_save_loginticketresponse", parse_and_save_loginticketresponse_mock):
                  
            resp = await client.post("/wsaa/loginCms")

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error generating access token."