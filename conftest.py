import pytest
from dotenv import load_dotenv

pytest_plugins = ["fixtures.api_fixtures", "fixtures.ui_fixtures"]

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
