from playwright.sync_api import sync_playwright, Page, expect

def verify_login_page(page: Page):
    """
    This script verifies the UI improvements on the login page.
    It navigates to the login page and takes a screenshot.
    """
    # 1. Navigate to the login page
    page.goto("http://localhost:5173/login")

    # 2. Assert that the main heading is visible
    # This ensures the page has loaded before taking the screenshot
    expect(page.get_by_role("heading", name="Welcome to Orion")).to_be_visible()

    # 3. Take a screenshot for visual verification
    page.screenshot(path="jules-scratch/verification/login_page.png")

# --- Boilerplate to run the verification ---
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_login_page(page)
        browser.close()

if __name__ == "__main__":
    main()