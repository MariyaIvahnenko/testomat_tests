import pytest
from playwright.sync_api import Page

from src.web.application import Application
from src.web.components.project_card import Badges


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    from src.web.application import Application

    return Application(page)


DEMO_PROJECT_NAME = "python manufacture"
DEFAULT_COMPANY = "QA Club Lviv"
EXPECTED_PLAN = "Enterprise plan"


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: Application):
    logged_app.projects_page.navigate()
    logged_app.projects_page.verify_page_loaded()

    logged_app.projects_page.header.get_selected_company("QA Club Lviv")
    logged_app.projects_page.header.get_plan_name("Enterprise plan")

    target_project_name = "aerodynamic rubber watch"
    logged_app.projects_page.header.search_projects(target_project_name)
    logged_app.projects_page.count_of_project_visible(1)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.Classical)
