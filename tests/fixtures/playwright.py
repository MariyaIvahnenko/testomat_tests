import pytest


@pytest.fixture(scope="session")
def browser_instance(browser):
    return browser

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
