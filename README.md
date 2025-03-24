# Django JSON Schema Editor

A powerful Django widget for integrating [`@json-editor/json-editor`](https://www.npmjs.com/package/@json-editor/json-editor) with Django forms and admin interfaces. It provides a rich, schema-based editing experience for JSON data in Django applications.

See [the blog post for the announcement and a screenshot](https://406.ch/writing/django-json-schema-editor/).

## Features

- Schema-based validation for JSON data
- Django admin integration
- Rich text editing capabilities with optional prose editor
- Foreign key references with Django admin lookups
- Referential integrity for JSON data containing model references

## Installation

```bash
pip install django-json-schema-editor
```

For django-prose-editor support (rich text editing):

```bash
pip install django-json-schema-editor[prose]
```

## Usage

### Basic Setup

1. Add `django_json_schema_editor` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_json_schema_editor',
    # ...
]
```

2. Use the `JSONField` in your models:

```python
from django.db import models
from django_json_schema_editor.fields import JSONField

class MyModel(models.Model):
    data = JSONField(
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "count": {"type": "integer"},
            },
        }
    )
```

### Rich Text Editing

For rich text editing, use the `prose` format:

```python
class MyModel(models.Model):
    data = JSONField(
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string", "format": "prose"},
            },
        }
    )
```

### Foreign Key References

You can reference Django models in your JSON data:

```python
class MyModel(models.Model):
    data = JSONField(
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "image": {
                    "type": "string",
                    "format": "foreign_key",
                    "options": {
                        "url": "/admin/myapp/image/?_popup=1&_to_field=id",
                    },
                },
            },
        }
    )
```

### Data References and Referential Integrity

One of the most powerful features is the ability to maintain referential integrity between JSON data and model instances:

```python
from django.db import models
from django_json_schema_editor.fields import JSONField

class Image(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='images/')

class Article(models.Model):
    data = JSONField(
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string", "format": "prose"},
                "featured_image": {
                    "type": "string",
                    "format": "foreign_key",
                    "options": {
                        "url": "/admin/myapp/image/?_popup=1&_to_field=id",
                    },
                },
            },
        }
    )

def get_image_ids(article):
    if image_id := article.data.get("featured_image"):
        return [int(image_id)]
    return []

# Register the reference to prevent images from being deleted when they're referenced
Article.register_data_reference(
    Image,
    name="featured_images",
    getter=get_image_ids,
)
```

This prevents a referenced image from being deleted as long as it's referenced in an article's JSON data.

The `name` field will be the name of the underlying `ManyToManyField` which actually references the `Image` instances.

## JSON Schema Support

The widget supports the [JSON Schema](https://json-schema.org/) standard for defining the structure and validation rules of your JSON data. Notable supported features include:

- Basic types: string, number, integer, boolean, array, object
- Format validations: date, time, email, etc.
- Custom formats: prose (rich text), foreign_key (model references)
- Required properties
- Enums and default values
- Nested objects and arrays

The [documentation for the json-editor](https://www.npmjs.com/package/@json-editor/json-editor) offers a good overview over all supported features.

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[tests,prose]"
```

### Code Quality

This project uses several tools to maintain code quality:

- **pre-commit**: We use pre-commit hooks to ensure consistent code style and quality
- **ruff**: For Python linting and formatting
- **biome**: For JavaScript and CSS linting and formatting

To set up pre-commit:

```bash
uv tool install pre-commit
pre-commit install
```

The pre-commit configuration includes:
- Basic file checks (trailing whitespace, merge conflicts, etc.)
- Django upgrade checks
- Ruff for Python linting and formatting
- Biome for JavaScript and CSS linting and formatting
- pyproject.toml validations

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
