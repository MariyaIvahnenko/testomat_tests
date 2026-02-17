from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config


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
