from functools import partial

from content_editor.admin import ContentEditorInline
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_json_schema_editor.fields import JSONField
from django_json_schema_editor.forms import JSONEditorField


class JSONPluginBase(models.Model):
    type = models.CharField(_("type"), max_length=1000, editable=False)
    data = JSONField(_("data"))

    class Meta:
        abstract = True

    def __str__(self):
        return ""

    def save(self, *args, **kwargs):
        self.type = self.TYPE
        super().save(*args, **kwargs)

    save.alters_data = True

    @classmethod
    def proxy(cls, type_name, *, schema, **meta):
        meta["proxy"] = True
        meta["app_label"] = cls._meta.app_label
        meta.setdefault("verbose_name", type_name)

        meta_class = type("Meta", (cls.Meta,), meta)

        return type(
            f"{cls.__qualname__}_{type_name}",
            (cls,),
            {
                "__module__": cls.__module__,
                "Meta": meta_class,
                "TYPE": type_name,
                "SCHEMA": schema,
            },
        )


class JSONPluginInline(ContentEditorInline):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=self.model.TYPE)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "data":
            kwargs["form_class"] = partial(JSONEditorField, schema=self.model.SCHEMA)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
