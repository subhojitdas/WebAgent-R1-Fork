from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--use-gl=egl"]
    )
    page = browser.new_page()
    page.goto("https://example.com", timeout=60000)
    page.screenshot(path="example.png")
    print("Title:", page.title())
    browser.close()
