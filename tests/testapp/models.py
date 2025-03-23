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
            },
        }
    )

    def __str__(self):
        return ""
