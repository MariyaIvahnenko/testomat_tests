import pytest
from playwright.sync_api import Page

import src.web.Application
from src.web.components.ProjectCard import Badges


@pytest.fixture(scope="function")
def app(page: Page) -> src.web.Application:
    from src.web.Application import Application
    return Application(page)


def test_projects_page_header(app: src.web.Application.Application, login):
    app.projects_page.navigate()

    app.projects_page.verify_page_loaded()

    app.projects_page.header.get_selected_company("QA Club Lviv")
    app.projects_page.header.get_plan_name("Enterprise plan")

    target_project_name = "aerodynamic rubber watch"
    app.projects_page.header.search_projects(target_project_name)
    app.projects_page.count_of_project_visible(1)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.Classical)
