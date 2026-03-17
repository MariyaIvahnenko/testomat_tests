from abc import ABC, abstractmethod
from typing import Self

import allure
from playwright.sync_api import Page


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    @allure.step
    def is_loaded(self) -> Self: ...

    @allure.step
    def wait_for_load(self, timeout: int = 30000) -> Self:
        """Wait for the page to finish loading."""
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        return self

    @allure.step
    def get_current_url(self) -> str:
        return self.page.url

    @allure.step
    def get_title(self) -> str:
        return self.page.title()

    @allure.step
    def take_screenshot(self, path: str) -> Self:
        self.page.screenshot(path=path)
        return self

    @allure.step
    def scroll_to_top(self) -> Self:
        self.page.evaluate("window.scrollTo(0, 0)")
        return self

    @allure.step
    def scroll_to_bottom(self) -> Self:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        return self
