from functools import partial

from django.db import models

from django_json_schema_editor.forms import JSONEditorField


class JSONField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self._config = kwargs.pop("config", None)
        self._schema = kwargs.pop("schema", None)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, "django.db.models.JSONField", args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault(
            "form_class",
            partial(JSONEditorField, config=self._config, schema=self._schema),
        )
        return super().formfield(**kwargs)
