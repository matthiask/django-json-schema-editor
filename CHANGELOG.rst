Change log
==========

Next version
~~~~~~~~~~~~

- Fixed the size of checkboxes in the JSON editor.
- Added configurable extensions support for the prose editor, allowing
  customization of available formatting options.


0.4 (2025-03-24)
~~~~~~~~~~~~~~~~

- Added a simple e2e test suite.
- Improved the prose editor integration, added the required importmap
  dependency.
- Expanded the README a lot.


0.3 (2025-03-20)
~~~~~~~~~~~~~~~~

- Fixed the JSON plugin data reference handling.
- Added a ``[prose]`` extra depending on the newest alpha version of
  django-prose-editor.


0.2 (2024-12-04)
~~~~~~~~~~~~~~~~

- Included the `django-prose-editor
  <https://django-prose-editor.readthedocs.io/>`__ support by default, it's a
  small file without much impact as long as the editor itself isn't loaded. The
  minimum supported version of django-prose-editor is 0.10a5.
- Updated the JSON editor to 2.15.2.


0.1 (2024-08-02)
~~~~~~~~~~~~~~~~

- Initial beta release.
