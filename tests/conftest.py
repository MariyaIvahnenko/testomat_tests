import asyncio
from pathlib import Path

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


@pytest.fixture(scope="session", autouse=True)
def disable_asyncio_for_sync_tests():
    """Автоматично вимикає asyncio для синхронних тестів"""
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            print("⚠️  Виявлено asyncio loop, створюємо новий потік")
            # Створюємо новий event loop в окремому потоці
            import threading
            def run_tests():
                pytest.main(["-m", "smoke"])

            thread = threading.Thread(target=run_tests)
            thread.start()
            thread.join()
            pytest.exit("Тести запущено в окремому потоці")
    except RuntimeError:
        pass  # Немає asyncio loop - все добре
