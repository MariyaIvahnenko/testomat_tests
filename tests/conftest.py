import os
from dataclasses import dataclass
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from src.web.Application import Application

load_dotenv(verbose=True)


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


def clear_cookies_and_storage(page: Page):
    # Clear cookies via context
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear(); window.sessionStorage.clear();")


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str

@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        login_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=100, timeout=30000, channel="chromium")
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def clean_app(browser_instance: Browser, configs: Config) -> Generator[Application, Any, None]:
    context = build_browser_instance(browser_instance, configs)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs: Config) -> BrowserContext:
    context = build_browser_instance(browser_instance, configs)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    # You may want to save storage state here if you intend to share state
    yield context
    page.close()
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext) -> Generator[Application, Any, None]:
    page = logged_context.new_page()
    yield Application(page)
    page.close()

@pytest.fixture(scope="session")
def build_browser_instance(browser_instance: Browser, configs: Config) -> BrowserContext:
    return browser_instance.new_context(
        base_url=configs.app_base_url,
        viewport={"width": 1920, "height": 1080},
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="test-result/videos/",
        permissions=["geolocation"],
    )


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs) -> Generator[Any, Any, None]:
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def app_for_invalid_login(shared_browser: Page) -> Generator[Application, Any, None]:
    """Provides a new Application for each invalid login test, using a fresh browser context."""
    app = Application(shared_browser)
    yield app
    clear_cookies_and_storage(shared_browser)
