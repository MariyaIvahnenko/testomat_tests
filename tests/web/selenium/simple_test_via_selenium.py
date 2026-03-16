import pytest
from faker import Faker
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.web.selenium.pages import LoginPage, LoginPageV2
from tests.fixtures.config import Config

fake = Faker()


@pytest.mark.regression
@pytest.mark.selenium
def test_selenium_login_and_search(driver: WebDriver, configs: Config):
    wait = WebDriverWait(driver, 10, 0.1, ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])

    driver.get(configs.login_url)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(By.CSS_SELECTOR, "#content-desktop [value = 'Sign In']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success")))

    target_project = "Gorgeous Rubber Coat"
    driver.find_element(By.CSS_SELECTOR, "#content-desktop #search").send_keys(target_project)
    driver.find_element(By.CSS_SELECTOR, f"#content-desktop [title = '{target_project}']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f".breadcrumbs-page [title='{target_project}']")))


def test_login_with_page_object_v1(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()


def test_login_with_page_object_v2(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()


def test_login_with_invalid_creds(driver, configs):
    login_page = LoginPage(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()

    invalid_password = Faker().password(length=10)
    login_page.login(configs.email, invalid_password)

    login_page.should_see_invalid_login_error()
