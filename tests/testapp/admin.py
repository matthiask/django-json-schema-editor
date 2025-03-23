from django.contrib import admin

from testapp import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Thing)
class ThingAdmin(admin.ModelAdmin):
    pass
