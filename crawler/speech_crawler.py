import io
from asyncio.exceptions import InvalidStateError
from playwright.sync_api import sync_playwright


def get_sentence_audio(sentence: str, audio_path: str) -> None:
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
            default_context = browser.contexts[0]
            page = default_context.pages[0]
            page.wait_for_timeout(500)

            page.locator("#inputDiv").fill(sentence)
            page.wait_for_timeout(500)

            with page.expect_request("blob:https://www.naturalreaders.com/*") as req:
                page.locator(".pw-read-btn").click()

            req_value = req.value
            resp = req_value.response()
            if resp.headers.get("content-type") == "audio/mpeg":
                audio_stream = io.BytesIO(resp.body())

                try:
                    with open(audio_path, "wb") as file:
                        file.write(audio_stream.getbuffer())
                except Exception as e:
                    print(e)

            page.wait_for_timeout(5000)

    except InvalidStateError:
        print("Daily Limit Reached")
        exit()
