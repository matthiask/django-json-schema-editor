import json
from copy import deepcopy

import fastjsonschema
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import get_language


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
        self._config = kwargs.pop("config", {})
        self._schema = kwargs.pop("schema")
        kwargs["widget"] = JSONEditorWidget
        super().__init__(*args, **kwargs)
        if self._config:
            self.widget.editor_config.update(self._config)
        if self._schema:
            self.widget.editor_config["schema"] = self._schema

    def clean(self, value):
        value = super().clean(value)
        try:
            fastjsonschema.validate(self._schema, value, use_formats=False)
        except fastjsonschema.JsonSchemaValueException as ex:
            raise ValidationError(ex.message) from ex
        return value


class JSONEditorWidget(forms.Textarea):
    template_name = "django_json_schema_editor/widget.html"
    supported_translations = {"de"}

    def __init__(self, *args, editor_config=None, **kwargs):
        self.editor_config = deepcopy(DEFAULT_CONFIG)
        if editor_config:
            self.editor_config.update(editor_config)
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["editor_config"] = json.dumps(self.editor_config, cls=DjangoJSONEncoder)
        return context

    @property
    def media(self):
        css = {
            "screen": ["django_json_schema_editor/django_theme.css"],
        }
        js = [
            "django_json_schema_editor/vendor/jsoneditor.js",
            "django_json_schema_editor/django_theme.js",
            "django_json_schema_editor/foreign_key.js",
            "django_json_schema_editor/widget.js",
        ]
        language = get_language()
        if language in self.supported_translations:
            js.append(f"django_json_schema_editor/language_{language}.js")
        return forms.Media(css=css, js=js)
