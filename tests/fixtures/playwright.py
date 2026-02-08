import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=0, timeout=30000, channel="chromium")
    yield browser
    browser.close()
