from functools import partial

from content_editor.admin import ContentEditorInline
from django.utils.translation import gettext_lazy as _
from feincms3.proxies import ProxyModelBase

from django_json_schema_editor.fields import JSONField
from django_json_schema_editor.forms import JSONEditorField


class JSONPluginBase(ProxyModelBase):
    data = JSONField(_("data"))

    class Meta:
        abstract = True

    def __str__(self):
        return ""

    @classmethod
    def proxy(cls, type_name, *, schema, **meta):
        return super().proxy(type_name, attrs={"SCHEMA": schema}, **meta)


class JSONPluginInline(ContentEditorInline):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=self.model.TYPE)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "data":
            kwargs["form_class"] = partial(JSONEditorField, schema=self.model.SCHEMA)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
