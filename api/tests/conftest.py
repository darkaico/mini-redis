import pytest

from api import app as api_app


@pytest.fixture
def api_client():
    api_app.app.config['TESTING'] = True

    with api_app.app.test_client() as client:
        yield client
