import json
from copy import deepcopy

from django import forms
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _, pgettext_lazy


JSONEDITOR_JS_URL = getattr(
    settings,
    "JSONEDITORWIDGET_JSONEDITOR_JS_URL",
    "https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js",  # noqa
)
DEFAULT_CONFIG = getattr(settings, "JSONEDITORWIDGET_DEFAULT_CONFIG", {})


class LazyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if any(
            isinstance(obj, t)
            for t in (
                type(_("dummy")),
                type(pgettext_lazy("dummy", "dummy")),
                type(capfirst(_("dummy"))),
                type(capfirst(pgettext_lazy("dummy", "dummy"))),
            )
        ):
            return force_str(obj)

        super().default(obj)


class JSONEditorWidget(forms.Textarea):
    template_name = "jsoneditorwidget/widget.html"

    class Media:
        js = (
            JSONEDITOR_JS_URL,
            "jsoneditorwidget/widget.js",
        )

    def __init__(self, *args, editor_config=None, **kwargs):
        self.editor_config = deepcopy(DEFAULT_CONFIG)
        if editor_config:
            self.editor_config.update(editor_config)
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["editor_config"] = json.dumps(self.editor_config, cls=LazyJSONEncoder)
        return context
