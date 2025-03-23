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

    # Go to the add page
    page.goto(f"{live_server.url}/admin/testapp/thing/{thing.pk}/change/")

    # Check that the prose editor is loaded
    editor_container = page.locator(".django_json_schema_editor")
    expect(editor_container).to_be_visible()

    prose_container = page.locator(".prose-editor")
    expect(prose_container).to_be_visible()
