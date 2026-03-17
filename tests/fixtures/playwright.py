import pytest


@pytest.fixture(scope="session")
def browser_instance(browser):
    return browser
