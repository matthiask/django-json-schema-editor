from django.db import models

from django_json_schema_editor.fields import JSONField


class File(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "file"

    def __str__(self):
        return self.name


class Thing(models.Model):
    data = JSONField(
        schema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "prose": {"type": "string", "format": "prose"},
                "file": {
                    "type": "string",
                    "format": "foreign_key",
                    "options": {
                        "url": "/admin/testapp/file/?_popup=1&_to_field=id",
                    },
                },
            },
        }
    )

    def __str__(self):
        return ""


def get_file_ids(plugin):
    if file := plugin.data.get("file"):
        return [int(file)]
    return []


Thing.register_data_reference(
    File,
    name="files",
    getter=get_file_ids,
)
