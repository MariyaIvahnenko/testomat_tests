import allure
from playwright.sync_api import Page, expect


class ProjectsPageHeader:
    def __init__(self, page: Page):
        self.page = page

        # Header elements
        self.page_title = page.locator("h2", has_text="Projects")
        self.enterprise_plan_label = page.get_by_text("Enterprise plan")
        self.free_plan_label = page.get_by_text("Free plan")
        self.company_selector = page.locator("#company_id")
        self.plan_badge = page.locator(".tooltip-project-plan")
        self.container = page.locator(".common-page-header")

        # Search
        self.search_input = page.locator("#search")

        # Action button
        self.create_button = page.locator("a.common-btn-primary", has_text="Create")
        self.manage_button = page.locator("a.common-btn-secondary", has_text="Manage")

        # View Toggle
        self.grid_view_button = page.locator("#grid-view")
        self.table_view_button = page.locator("#table-view")

    @allure.step
    def select_company(self, company_name: str):
        self.company_selector.select_option(label=company_name)

    @allure.step
    def search_projects(self, query: str):
        self.search_input.fill(query)

    @allure.step
    def click_create(self):
        self.create_button.click()

    @allure.step
    def click_manage(self):
        self.manage_button.click()

    @allure.step
    def switch_to_grid_view(self):
        self.grid_view_button.click()

    @allure.step
    def switch_to_table_view(self):
        self.table_view_button.click()

    @allure.step
    def get_selected_company(self, expected_value: str):
        expect(self.company_selector.locator("option[selected]")).to_have_text(expected_value)

    @allure.step
    def get_plan_name(self, expected_value: str):
        return expect(self.plan_badge.locator("span").last).to_have_text(expected_value)
