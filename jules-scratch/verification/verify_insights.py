from playwright.sync_api import sync_playwright, expect

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. Navigate directly to the insights page
            page.goto("http://localhost:5173/insights", timeout=60000)

            # 2. Verify that the chart components are visible
            expect(page.get_by_role("heading", name="Spending Over Time")).to_be_visible()
            expect(page.get_by_role("heading", name="Spending by Category")).to_be_visible()

            # 3. Add a short delay to allow charts to render
            page.wait_for_timeout(1000)

            # 4. Take a screenshot
            page.screenshot(path="jules-scratch/verification/insights.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    main()