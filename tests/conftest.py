import os
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient
from pytest_httpserver import HTTPServer

from config.paths import AfipPaths
from service.api.app import app
from service.soap_client.async_client import WSFEClientManager
from service.utils.jwt_validator import verify_token

import logging

# Zeep logs for debugging
# logging.getLogger("zeep").setLevel(logging.DEBUG)
# logging.getLogger("zeep.transports").setLevel(logging.DEBUG)
# logging.getLogger("zeep.client").setLevel(logging.DEBUG)
# logging.getLogger("zeep.wsdl").setLevel(logging.DEBUG)


# Avoid endpoint Depends=verify_jwt() verification
@pytest.fixture
def override_auth():

    async def fake_verify():
        return {"user" : "test-user", "roles" : ["test"]}
    
    app.dependency_overrides[verify_token] = fake_verify
    yield
    app.dependency_overrides.pop(verify_token, None)


# Use test paths for mock xml files
@pytest.fixture
def afip_paths():
    mocks = Path(__file__).parent / "mocks"
    return AfipPaths(
        base_xml=mocks,
        base_crypto=mocks,
        base_certs=mocks,
    )


# Patch the paths
@pytest.fixture(autouse=True)
def override_afip_paths(afip_paths, monkeypatch):
    monkeypatch.setattr("config.paths.get_afip_paths", lambda: afip_paths)


# Create FasAPI testing client
@pytest.fixture
def client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test")


# Force http server at 62768
@pytest.fixture
def httpserver_fixed_port():
    server = HTTPServer(port=62768)
    server.start()
    yield server
    server.stop()


# Initialize zeep client only if httpserver is created
@pytest_asyncio.fixture
async def wsfe_manager(httpserver_fixed_port):
    WSFEClientManager.reset_singleton()

    afip_wsdl = os.path.join("tests\\mocks", "wsfe_mock.wsdl")
    manager = WSFEClientManager(afip_wsdl)
    yield manager
    await manager.close()

    WSFEClientManager.reset_singleton()