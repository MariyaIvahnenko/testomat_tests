from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.application import Application

PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"

load_dotenv(verbose=True)


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


def clear_cookies_and_storage(page: Page):
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear(); window.sessionStorage.clear();")


PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"


def pytest_configure(config: pytest.Config) -> None:
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override browser context args for CI"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.app",
    "tests.fixtures.api",
    "tests.fixtures.selenium",
]


@pytest.fixture(scope="function", autouse=True)
def wait_between_tests():
    import time
    time.sleep(1)
    yield
