import pyperclip
from playwright.sync_api import sync_playwright


def gpt_crawler(prompt: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        default_context = browser.contexts[0]
        page = default_context.pages[1]

        input_text = page.locator("#prompt-textarea")
        input_text.fill(prompt)
        input_text.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        div = page.locator(".rounded-xl").last
        div.locator(".items-center").get_by_role("button").locator("nth=1").click()

        return pyperclip.paste()
