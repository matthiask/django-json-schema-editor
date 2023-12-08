import json
from copy import deepcopy

from django import forms
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


DEFAULT_CONFIG = getattr(settings, "JSONEDITORWIDGET_DEFAULT_CONFIG", {})


class JSONEditorWidget(forms.Textarea):
    template_name = "jsoneditorwidget/widget.html"

    class Media:
        js = (
            settings.JSONEDITORWIDGET_JSONEDITOR_JS_URL,
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
