import os

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        is_ci = os.getenv("CI", "false").lower() == "true"

        browser = p.chromium.launch(headless=is_ci, slow_mo=0, timeout=30000)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance):
    context = browser_instance.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
