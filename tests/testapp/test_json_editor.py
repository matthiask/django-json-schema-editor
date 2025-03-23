import os

import pytest
from playwright.sync_api import expect

from testapp.models import Thing


# Set Django async unsafe to allow database operations in tests
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


def login_admin(page, live_server):
    """Helper function to login as admin."""
    from django.contrib.auth.models import User

    # Delete any existing superusers with the same username to avoid conflicts
    User.objects.filter(username="admin").delete()

    User.objects.create_superuser("admin", "admin@example.com", "password")
    page.goto(f"{live_server.url}/admin/login/")
    page.fill("#id_username", "admin")
    page.fill("#id_password", "password")
    page.click("input[type=submit]")
    page.wait_for_url(f"{live_server.url}/admin/")


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_admin_form(page, live_server):
    """Test that the JSON editor is loaded in the admin form."""
    login_admin(page, live_server)

    # Go to the add page
    page.goto(f"{live_server.url}/admin/testapp/thing/add/")

    # Check that the prose editor is loaded
    editor_container = page.locator(".django_json_schema_editor")
    expect(editor_container).to_be_visible()


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_prose(page, live_server):
    """Test that prose editor loads and displays content correctly."""
    login_admin(page, live_server)

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


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_edit_save(page, live_server):
    """Test editing and saving content in the JSON editor."""
    login_admin(page, live_server)

    thing = Thing.objects.create(
        data={
            "text": "Original text",
            "prose": "Original prose",
        }
    )

    # Go to the change page
    page.goto(f"{live_server.url}/admin/testapp/thing/{thing.pk}/change/")
    page.wait_for_timeout(1000)  # Wait for editor to initialize

    # Edit the regular text field
    text_input = page.locator('input[id="root[text]"]')
    expect(text_input).to_be_visible()
    text_input.fill("Updated text")

    # Edit the prose field - focus on the element first
    prose_editor = page.locator(".prose-editor .ProseMirror")
    expect(prose_editor).to_be_visible()
    prose_editor.click()

    # Clear the content and type new content
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.type("New prose content")

    # Submit the form to save changes
    page.click('input[name="_save"]')

    # Navigate back to the object to verify the changes were saved
    page.goto(f"{live_server.url}/admin/testapp/thing/{thing.pk}/change/")
    page.wait_for_timeout(1000)

    # Verify text field was updated
    text_input = page.locator('input[id="root[text]"]')
    expect(text_input).to_have_value("Updated text")

    # Verify prose field was updated
    prose_editor = page.locator(".prose-editor .ProseMirror")
    expect(prose_editor).to_contain_text("New prose content")

    # Verify the underlying JSON data
    textarea = page.locator("textarea#id_data")
    textarea_value = textarea.input_value()
    textarea_json = page.evaluate("value => JSON.parse(value)", textarea_value)
    assert textarea_json["text"] == "Updated text"
    assert "New prose content" in textarea_json["prose"]


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_display(page, live_server):
    """Test that the JSON schema editor correctly displays data."""
    login_admin(page, live_server)

    # Create a test object directly via Django model
    test_data = {"text": "Test text field", "prose": "<p>Test prose content</p>"}
    Thing.objects.create(data=test_data)

    # Go directly to the edit page for the first Thing object
    thing = Thing.objects.first()
    page.goto(f"{live_server.url}/admin/testapp/thing/{thing.pk}/change/")

    # Wait for editor to initialize
    page.wait_for_timeout(1000)

    # Verify that text field displays our test data
    text_input = page.locator('input[id="root[text]"]')
    expect(text_input).to_be_visible()
    expect(text_input).to_have_value("Test text field")

    # Verify that prose field contains our test content
    prose_editor = page.locator(".prose-editor .ProseMirror")
    expect(prose_editor).to_be_visible()
    expect(prose_editor).to_contain_text("Test prose content")


@pytest.mark.django_db
@pytest.mark.e2e
def test_json_editor_ui_elements(page, live_server):
    """Test UI elements of the JSON editor like toolbar buttons."""
    login_admin(page, live_server)

    # Go to the add page
    page.goto(f"{live_server.url}/admin/testapp/thing/add/")
    page.wait_for_timeout(1000)  # Wait for editor to initialize

    # Verify the editor has loaded and the UI elements are present

    # Prose editor toolbar should be visible
    toolbar = page.locator(".prose-menubar")
    expect(toolbar).to_be_visible()

    # Check that formatting buttons exist and are visible
    expect(page.locator(".prose-menubar__button[title='bold']")).to_be_visible()
    expect(page.locator(".prose-menubar__button[title='italic']")).to_be_visible()
    expect(page.locator(".prose-menubar__button[title='underline']")).to_be_visible()

    # Verify the text editor field is present
    text_input = page.locator('input[id="root[text]"]')
    expect(text_input).to_be_visible()

    # Focus on the prose editor
    prose_editor = page.locator(".prose-editor .ProseMirror")
    expect(prose_editor).to_be_visible()
    prose_editor.click()

    # Type some text
    page.keyboard.type("Testing formatting")

    # Select the text
    page.keyboard.press("Control+A")

    # Click the bold button in the prose editor toolbar
    bold_button = page.locator(".prose-menubar__button[title='bold']")
    bold_button.click()

    # Verify the text is now bold (check in the DOM)
    prose_html = prose_editor.inner_html()
    assert "<strong>Testing formatting</strong>" in prose_html
