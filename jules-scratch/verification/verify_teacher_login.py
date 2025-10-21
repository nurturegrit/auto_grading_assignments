from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5000/teacher_login")
    page.get_by_label("Email").fill("teacher@example.com")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Login").click()
    page.screenshot(path="jules-scratch/verification/teacher_login.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
