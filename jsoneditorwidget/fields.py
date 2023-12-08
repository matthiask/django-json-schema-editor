from functools import partial

from django.db import models

from jsoneditorwidget.forms import JSONEditorField


class JSONField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self._schema = kwargs.pop("schema")
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = [("", "")]
        return name, "django.db.models.JSONField", args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", partial(JSONEditorField, schema=self._schema))
        return super().formfield(**kwargs)
