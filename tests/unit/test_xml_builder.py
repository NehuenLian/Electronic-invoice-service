from service.xml_management.xml_builder import build_login_ticket_request, parse_and_save_loginticketresponse


def test_build_login_ticket_request():

    def fake_time_provider():
        return (
            1767764408,
            "2026-01-07T05:40:08Z",
            "2026-01-07T05:50:08Z",
        )

    root = build_login_ticket_request(fake_time_provider)

    assert root.find("header/uniqueId").text == "1767764408"
