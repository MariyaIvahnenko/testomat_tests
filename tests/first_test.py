import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

LOGIN_URL = f"{os.getenv("BASE_APP_URL")}/users/sign_in"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def test_login_with_invalid_creds(page: Page):
    page.goto(os.getenv("BASE_URL"))

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()
    login_user(page, EMAIL, "12131415")

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator('#content-desktop .common-flash-info')).to_have_text("Invalid Email or password.")

    expect(page).to_have_title("Testomat.io")


def test_search_non_existing_project(page: Page):
    page.goto(LOGIN_URL)
    login_user(page, EMAIL, PASSWORD)

    non_existing_project = "python manufacture"
    search_for_non_existing_project(page, non_existing_project)

    expect(page.get_by_role("heading", name=non_existing_project)).to_have_count(0)


def test_search_project_in_company(page: Page):
    page.goto(LOGIN_URL)
    login_user(page, EMAIL, PASSWORD)

    target_project = "aerodynamic rubber watch"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_visible()

    expect(page.locator("ul li h3", has_text=target_project)).to_be_visible()
    expect(page.locator("ul li h3").filter(has_text="Industrial & Jewelry")).to_have_text("Industrial & Jewelry")


def test_should_be_possible_to_open_free_project(page: Page):
    page.goto(LOGIN_URL)
    login_user(page, EMAIL, PASSWORD)

    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    target_project = "aerodynamic rubber watch"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=100)


def test_presence_button_create_company_to_upgrade(page: Page):
    page.goto(LOGIN_URL)
    login_user(page, EMAIL, PASSWORD)

    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    expect(page.get_by_role("link", name="Create Company to Upgrade")).to_be_visible()


def test_checking_the_documentation_page(page: Page):
    page.goto(LOGIN_URL)
    login_user(page, EMAIL, PASSWORD)

    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")
    page.locator("a", has_text="Read docs →").click()

    expect(page.locator("h1").filter(has_text="Testomat.io Docs")).to_have_text("Testomat.io Docs")


def search_for_project(page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def search_for_non_existing_project(page, non_existing_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(non_existing_project)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()
