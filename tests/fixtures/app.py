import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import (
    CookieHelper,
    clear_cookies_and_storage,
)

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH = Path("test-result/.auth/free_project_state.json")


def create_free_project_state() -> None:
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_instance(
        browser: Browser,
        base_url: str,
        storage_state: Path | None = None,
) -> BrowserContext:
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    return browser.new_context(**kwargs)


@pytest.fixture(scope="function")
def clean_app(browser_instance: Browser, configs: Config, build_browser_instance) -> Generator[Application, Any]:
    context = build_browser_instance
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs: Config) -> Page:
    if STORAGE_STATE_PATH.exists():
        context = build_browser_instance(browser_instance, configs.login_url, storage_state=STORAGE_STATE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_instance(browser_instance, configs.login_url, storage_state=STORAGE_STATE_PATH)
    yield context.new_page()
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)
    create_free_project_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: Page) -> Application:
    logged_context.goto("/projects")
    yield Application(logged_context)


@pytest.fixture(scope="function")
def cookies(logged_context: Page) -> CookieHelper:
    return CookieHelper(logged_context.context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs) -> Page:
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def app_for_invalid_login(shared_browser: Page) -> Application:
    app = Application(shared_browser)
    yield app
    clear_cookies_and_storage(shared_browser)


@pytest.fixture(scope="session")
def free_project_page(logged_context: BrowserContext, browser_instance: Browser, configs) -> Page:
    if FREE_PROJECT_STORAGE_PATH.exists():
        context = build_browser_instance(browser_instance, configs.login_url, storage_state=FREE_PROJECT_STORAGE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_instance(browser_instance, configs.app_base_url)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    app.projects_page.is_loaded()
    app.projects_page.open()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=FREE_PROJECT_STORAGE_PATH)

    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page) -> Application:
    free_project_page.goto("/projects")
    yield Application(free_project_page)
    free_project_page.close()
