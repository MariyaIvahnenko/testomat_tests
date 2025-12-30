from playwright.sync_api import Page, expect

def test_login_with_invalid_creds(page: Page):
    page.goto("https://testomat.io/")

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    page.locator("#content-desktop #user_email").fill("maryivahnenko@gmail.com")
    page.locator("#content-desktop #user_password").fill("121314")
    page.get_by_role("button", name="Sign in").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator('#content-desktop .common-flash-info')).to_have_text("Invalid Email or password.")

    expect(page).to_have_title("Testomat.io")