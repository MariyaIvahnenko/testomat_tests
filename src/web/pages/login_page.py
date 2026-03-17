from typing import Self

import allure
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step
    def open(self):
        self.page.goto("/users/sign_in")

    @allure.step
    def is_loaded(self):
        expect(self.page.locator("#content-desktop form#new_user")).to_be_visible()

    @allure.step
    def login(self, email: str, password: str):
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    @allure.step
    def invalid_login_message_visible(self) -> Self:
        expect(self.page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
        return self
