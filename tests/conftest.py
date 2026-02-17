import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.application import Application

load_dotenv(verbose=True)

@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


def clear_cookies_and_storage(page: Page):
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear(); window.sessionStorage.clear();")

pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.app",
    "tests.fixtures.api",
    "tests.fixtures.selenium",
]
