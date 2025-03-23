import os

import pytest
from playwright.sync_api import expect

from testapp.models import Thing


# Set Django async unsafe to allow database operations in tests
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_admin_form(page, live_server):
    # Login first
    from django.contrib.auth.models import User

    User.objects.create_superuser("admin", "admin@example.com", "password")

    # Visit the login page
    page.goto(f"{live_server.url}/admin/login/")

    # Fill in the login form
    page.fill("#id_username", "admin")
    page.fill("#id_password", "password")

    # Submit the form
    page.click("input[type=submit]")

    # Wait for the admin index page to load
    page.wait_for_url(f"{live_server.url}/admin/")

    # Go to the add page
    page.goto(f"{live_server.url}/admin/testapp/thing/add/")

    # Check that the prose editor is loaded
    editor_container = page.locator(".django_json_schema_editor")
    expect(editor_container).to_be_visible()


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_prose(page, live_server):
    # Login first
    from django.contrib.auth.models import User

    User.objects.create_superuser("admin", "admin@example.com", "password")

    # Visit the login page
    page.goto(f"{live_server.url}/admin/login/")

    # Fill in the login form
    page.fill("#id_username", "admin")
    page.fill("#id_password", "password")

    # Submit the form
    page.click("input[type=submit]")

    # Wait for the admin index page to load
    page.wait_for_url(f"{live_server.url}/admin/")

    thing = Thing.objects.create(
        data={
            "text": "Hello World",
            "prose": "<strong>Prose</strong> is <em>fine</em>",
        }
    )

    # Go to the change page
    page.goto(f"{live_server.url}/admin/testapp/thing/{thing.pk}/change/")

    # Check that the prose editor is loaded
    editor_container = page.locator(".django_json_schema_editor")
    expect(editor_container).to_be_visible()

    # Check that the prose editor contains the expected content
    prose_container = page.locator(".prose-editor")
    expect(prose_container).to_be_visible()

    # Wait for the editor to fully initialize
    page.wait_for_timeout(1000)

    # Verify the hidden textarea with our JSON data
    textarea = page.locator("textarea#id_data")
    # The textarea is hidden, so we don't check visibility
    textarea_value = textarea.input_value()
    textarea_json = page.evaluate("value => JSON.parse(value)", textarea_value)
    assert textarea_json["text"] == "Hello World"
    assert textarea_json["prose"] == "<strong>Prose</strong> is <em>fine</em>"

    # Find the JSON editor object container
    editor_container = page.locator(".je-object__container")
    expect(editor_container).to_be_visible()

    # Check for the text field using the exact ID from the HTML
    text_input = page.locator('input[id="root[text]"]')
    expect(text_input).to_be_visible()
    expect(text_input).to_have_value("Hello World")

    # Check for the prose content using the exact selector from the HTML
    prose_editor = page.locator(".prose-editor .ProseMirror")
    expect(prose_editor).to_be_visible()

    # Check if the prose editor contains our expected text
    expect(prose_editor).to_contain_text("Prose is fine")

    # Verify the HTML content
    prose_html = prose_editor.inner_html()
    assert "<strong>Prose</strong>" in prose_html
    assert "<em>fine</em>" in prose_html
