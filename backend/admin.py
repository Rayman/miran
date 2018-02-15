from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Item, Attribute


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    # fk_name = 'user'
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)


class AttributeInline(admin.TabularInline):
    model = Attribute


class ItemAdmin(admin.ModelAdmin):
    inlines = (AttributeInline, )


admin.site.register(Item, ItemAdmin)
