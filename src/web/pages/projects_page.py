from ast import List

import allure
from playwright.sync_api import Page, expect

from src.web.components.project_card import ProjectCard
from src.web.components.projects_page_header import ProjectsPageHeader


class ProjectsPage:
    def __init__(self, page: Page, base_url: str = "https://app.testomat.io"):
        self.page = page
        self.header = ProjectsPageHeader(page)
        self.base_url = base_url

        self.info_message = page.locator(".common-flash-info-right p")
        self.success_message = page.locator(".common-flash-success-right p")

        self.project_grid = page.locator("#grid")
        self._project_cards = page.locator('#grid ul li.relative:has(a[href*="/projects/"])')

        # Notice about uninvited projects
        self.uninvited_notice = page.locator("li span.text-gray-400")

        # Total counter
        self.total_count = page.locator(".common-counter")

    def navigate(self):
        url = f"{self.base_url}/projects"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step
    def get_success_massage(self) -> str:
        return self.success_message.text_content().strip()

    @allure.step
    def get_projects(self) -> List[ProjectCard]:
        return [ProjectCard(card) for card in self._project_cards.all()]

    @allure.step
    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self._project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        return ProjectCard(card)

    @allure.step
    def get_total_projects(self) -> int:
        return int(self.total_count.text_content())

    @allure.step
    def search_and_get_result(self, query: str) -> List[ProjectCard]:
        self.header.search_projects(query)
        # Wait for search to complete
        self.page.wait_for_timeout(300)
        return self.get_projects()

    @allure.step
    def verify_page_loaded(self):
        expect(self.header.page_title).to_be_visible()
        expect(self.project_grid).to_be_visible()

    @allure.step
    def count_of_project_visible(self, expected_count: int):
        return expect(self._project_cards.filter(visible=True)).to_have_count(expected_count)

    @allure.step
    def verify_success_message(self, expected_text: str):
        expect(self.success_message).to_have_text(expected_text)

    @allure.step
    def get_demo_projects(self, expected_text: str) -> List[ProjectCard]:
        return [project for project in self.get_projects() if project.is_demo_project()]

    @allure.step
    def is_loaded(self):
        expect(self.page.locator(".common-flash-success")).to_be_visible()
        expect(self.page.locator(".common-flash-success")).to_have_text("Signed in successfully")

        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()
