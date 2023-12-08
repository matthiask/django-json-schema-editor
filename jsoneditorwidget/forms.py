import json
from copy import deepcopy

from django import forms
from django.conf import settings
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


class JSONEditorWidget(forms.Textarea):
    template_name = "jsoneditorwidget/widget.html"

    class Media:
        css = {
            "screen": ["jsoneditorwidget/django_theme.css"],
        }
        js = (
            "https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js",
            "jsoneditorwidget/django_theme.js",
            "jsoneditorwidget/widget.js",
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
