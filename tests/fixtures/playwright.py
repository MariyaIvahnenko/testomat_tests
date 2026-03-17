# import os

import pytest


# from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance(browser):
    return browser
