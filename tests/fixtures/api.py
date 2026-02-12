import os

import pytest
from dotenv import load_dotenv

from src.api.client import TestomatClient

load_dotenv()


@pytest.fixture(scope="session")
def api_credentials():
    base_url = os.getenv("BASE_APP_URL")
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    if not all([base_url, email, password]):
        pytest.fail(
            "Missing required environment variables. "
            "Please ensure BASE_APP_URL, EMAIL, and PASSWORD are set in .env file"
        )

    return {
        "email": email,
        "password": password,
        "base_url": base_url
    }


@pytest.fixture(scope="session")
def api_token(api_credentials):
    client = TestomatClient()
    client.email = api_credentials["email"]
    client.password = api_credentials["password"]
    client.base_url = api_credentials["base_url"]

    success = client.login()

    if not success or not client.jwt_token:
        pytest.fail("Failed to obtain API token during test setup")

    return client.jwt_token


@pytest.fixture
def api_client(api_credentials):
    client = TestomatClient()
    client.email = api_credentials["email"]
    client.password = api_credentials["password"]
    client.base_url = api_credentials["base_url"]

    success = client.login()

    if not success:
        pytest.fail("Failed to authenticate client during test setup")

    return client


@pytest.fixture
def unauthenticated_client(api_credentials):
    client = TestomatClient()
    client.email = api_credentials["email"]
    client.password = api_credentials["password"]
    client.base_url = api_credentials["base_url"]

    return client
