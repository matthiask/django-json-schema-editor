import os

import pytest


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    """Modify browser context arguments for tracing."""
    return {
        **browser_context_args,
        "record_video_dir": os.path.join(os.getcwd(), "test-results/videos/"),
        "record_har_path": os.path.join(os.getcwd(), "test-results/har/", "test.har"),
    }


@pytest.fixture(scope="function")
def page(page):
    """Configure page to capture console logs."""
    console_messages = []

    def handle_console(msg):
        console_messages.append(f"[{msg.type.upper()}] {msg.text}")
        # Print to stdout immediately so it appears in test output
        print(f"BROWSER CONSOLE [{msg.type.upper()}]: {msg.text}")

    page.on("console", handle_console)

    # Store console messages on the page object for later access
    page.console_messages = console_messages

    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Handle reporting and artifact generation."""
    outcome = yield
    report = outcome.get_result()

    # Take screenshot of failed tests and capture console logs
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs["page"]

            # Print console logs for failed tests
            if hasattr(page, "console_messages") and page.console_messages:
                print(f"\n=== Console logs for failed test '{item.name}' ===")
                for msg in page.console_messages:
                    print(msg)
                print("=== End console logs ===\n")

            # Take screenshot and save it with test name
            screenshot_dir = os.path.join(os.getcwd(), "test-results/screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_failed.png")
            page.screenshot(path=screenshot_path)
            # Save page HTML
            html_path = os.path.join(screenshot_dir, f"{item.name}_failed.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(page.content())

            # Save console logs to file
            if hasattr(page, "console_messages") and page.console_messages:
                console_log_path = os.path.join(
                    screenshot_dir, f"{item.name}_console.log"
                )
                with open(console_log_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(page.console_messages))

            # Add to report
            report.extra = [
                {
                    "name": "Screenshot",
                    "content": screenshot_path,
                    "mime_type": "image/png",
                },
                {"name": "HTML", "content": html_path, "mime_type": "text/html"},
            ]
        except Exception as e:
            print(f"Failed to capture artifacts: {e}")
