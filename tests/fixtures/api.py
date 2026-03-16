import os

import pytest
import requests

from api.client import TestomatClient
from src.api.controllers import ProjectController, SuiteController, TestController
from src.api.models import Project
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def auth_token(configs: Config) -> str:
    response = requests.post(
        f"{configs.login_url}/api/login",
        json={"api_token": configs.testomat_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["jwt"]


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


@pytest.fixture(scope="session")
def project_controller(configs: Config, auth_token: str) -> ProjectController:
    controller = ProjectController(
        login_url=configs.login_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def suite_controller(configs: Config, auth_token: str) -> SuiteController:
    controller = SuiteController(
        login_url=configs.login_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def test_controller(configs: Config, auth_token: str) -> TestController:
    controller = TestController(
        login_url=configs.login_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="function")
def project(project_controller: ProjectController) -> Project:
    projects = project_controller.get_all()
    return projects[0]
