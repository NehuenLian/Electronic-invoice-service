from unittest.mock import patch

from service.payload_builder.builder import add_auth_to_payload


def test_add_auth_to_payload():

    fake_sale_data = { "Auth": {} }
    fake_token = "fake_token"
    fake_sign = "fake_sign"

    fake_sale_data_with_auth = add_auth_to_payload(fake_sale_data, "fake_token", "fake_sign")

    assert fake_sale_data_with_auth['Auth']['Token'] == fake_token
    assert fake_sale_data_with_auth['Auth']['Sign'] == fake_sign