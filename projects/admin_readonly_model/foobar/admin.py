from django.contrib import admin

from .models import Foo, Bar


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Bar._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
