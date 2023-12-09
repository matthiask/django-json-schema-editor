import json
from copy import deepcopy

import fastjsonschema
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder


DEFAULT_CONFIG = getattr(
    settings,
    "JSONEDITORWIDGET_DEFAULT_CONFIG",
    {
        "disable_properties": True,
        "disable_collapse": True,
        # "disable_edit_json": True,
        "display_required_only": False,
        "theme": "django",
    },
)


class JSONEditorField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        self._schema = kwargs.pop("schema")
        kwargs["widget"] = JSONEditorWidget
        super().__init__(*args, **kwargs)
        self.widget.editor_config["schema"] = self._schema

    def clean(self, value):
        value = super().clean(value)
        try:
            fastjsonschema.validate(self._schema, value, use_formats=False)
        except fastjsonschema.JsonSchemaValueException as ex:
            raise ValidationError({"data": ex.message}) from ex
        return value


class JSONEditorWidget(forms.Textarea):
    template_name = "django_json_schema_editor/widget.html"

    class Media:
        css = {
            "screen": ["django_json_schema_editor/django_theme.css"],
        }
        js = (
            "django_json_schema_editor/vendor/jsoneditor.js",
            "django_json_schema_editor/django_theme.js",
            "django_json_schema_editor/widget.js",
        )

    def __init__(self, *args, editor_config=None, **kwargs):
        self.editor_config = deepcopy(DEFAULT_CONFIG)
        if editor_config:
            self.editor_config.update(editor_config)
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["editor_config"] = json.dumps(self.editor_config, cls=DjangoJSONEncoder)
        return context
