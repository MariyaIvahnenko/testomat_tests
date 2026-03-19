from playwright.sync_api import BrowserContext, Cookie, Page


class CookieHelper:
    def __init__(self, context: BrowserContext):
        self.context = context

    def add(
        self,
        name: str,
        value: str,
        domain: str,
        path: str = "/",
        *,
        http_only: bool = False,
        secure: bool = False,
        same_site: str = "Lax",
        expires: float | None = None,
    ) -> None:
        cookie: Cookie = {
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
            "httpOnly": http_only,
            "secure": secure,
            "sameSite": same_site,
        }
        if expires:
            cookie["expires"] = expires
        self.context.add_cookies([cookie])

    def add_many(self, cookies: list[Cookie]) -> None:
        self.context.add_cookies(cookies)

    def get_all(self, urls: list[str] | None = None) -> list[Cookie]:
        return self.context.cookies(urls) if urls else self.context.cookies()

    def get(self, name: str) -> Cookie | None:
        for cookie in self.context.cookies():
            if cookie["name"] == name:
                return cookie
        return None

    def get_value(self, name: str) -> str | None:
        cookie = self.get(name)
        return cookie["value"] if cookie else None

    def exists(self, name: str) -> bool:
        return self.get(name) is not None

    def clear_all(self) -> None:
        self.context.clear_cookies()

    def clear(self, *, name: str | None = None, domain: str | None = None, path: str | None = None) -> None:
        self.context.clear_cookies(name=name, domain=domain, path=path)


def clear_cookies_and_storage(page: Page) -> None:
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")
