import pytest

from src.web.application import Application
from tests.conftest import Config
from tests.first_test import fake

invalid_login_test_data = [
    pytest.param("", "", id="empty_email_and_password"),
    pytest.param("", fake.password(length=8), id="empty_email"),
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param("plainstring", fake.password(length=8), id="not_email_format"),
    pytest.param(fake.email(), "1234", id="short_password_below_min"),
    pytest.param(fake.email(), fake.password(length=64), id="long_password_above_max"),
    pytest.param(fake.user_name(), fake.password(length=10), id="username_as_email"),
    pytest.param(fake.email(), fake.password(length=8), id="random_email_random_password"),
    pytest.param(fake.email(), fake.password(length=100), id="random_email_long_password"),
    pytest.param(fake.email(), "<script>alert('xss')</script>", id="xss_password"),
    pytest.param(fake.email(), "' OR 1=1;--", id="sql_injection_password"),
]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email,password", invalid_login_test_data)
def test_login_invalid(app_for_invalid_login: Application, configs: Config, email: str, password: str):
    app_for_invalid_login.home_page.open()
    app_for_invalid_login.home_page.is_loaded()
    app_for_invalid_login.home_page.click_login()

    app_for_invalid_login.login_page.is_loaded()
    app_for_invalid_login.login_page.login(email, password)
    app_for_invalid_login.login_page.invalid_login_message_visible()
    app_for_invalid_login.page.wait_for_timeout(2000)


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(app: Application, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    app.projects_page.is_loaded()
