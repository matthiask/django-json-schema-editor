from functools import partial

from django.db import models
from django.db.models import Q, signals

from django_json_schema_editor.forms import JSONEditorField


def _register_reference(jsonmodel, to, *, name, getter):
    class Meta:
        verbose_name = f"{jsonmodel.__name__} ⇒ {to.__name__} reference"

    ns = {
        "__module__": jsonmodel.__module__,
        "parent": models.ForeignKey(
            jsonmodel, on_delete=models.CASCADE, related_name="+"
        ),
        "object": models.ForeignKey(to, on_delete=models.PROTECT, related_name="+"),
        "Meta": Meta,
        "__str__": lambda obj: str(obj.parent),
    }

    reference = type(
        f"{jsonmodel._meta.model_name}_{to._meta.label_lower.replace('.', '_')}_ref",
        (models.Model,),
        ns,
    )

    def listener(sender, instance, **kwargs):
        if not isinstance(instance, jsonmodel):
            return

        if (data := getter(instance)) is None or not isinstance(data, list):
            return

        pks = [pk for pk in data if pk]
        for pk in pks:
            reference.objects.update_or_create(parent=instance, object_id=pk)
        reference.objects.filter(Q(parent=instance) & ~Q(object_id__in=pks)).delete()

    # This doesn't work because we're using proxy models:
    # signals.post_save.connect(listener, sender=jsonmodel, weak=False)
    signals.post_save.connect(listener, weak=False)

    models.ManyToManyField(to, editable=False, through=reference).contribute_to_class(
        jsonmodel, name
    )


class JSONField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self._config = kwargs.pop("config", None)
        self._schema = kwargs.pop("schema", None)
        self._foreign_key_descriptions = kwargs.pop("foreign_key_descriptions", [])
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, "django.db.models.JSONField", args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault(
            "form_class",
            partial(
                JSONEditorField,
                config=self._config,
                schema=self._schema,
                foreign_key_descriptions=self._foreign_key_descriptions,
            ),
        )
        return super().formfield(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, f"register_{name}_reference", partial(_register_reference, cls))
