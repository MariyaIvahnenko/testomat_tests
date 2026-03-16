import pytest
import requests

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
