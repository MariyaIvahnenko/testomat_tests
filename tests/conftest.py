import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.Application import Application

load_dotenv(verbose=True)

@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str

@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        login_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(app: Application,
          configs: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chromium",
        "headless": True,
        "slow_mo": 100,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_ergs(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk_UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }
