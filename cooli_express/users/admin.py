import random
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from cooli_express.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name", "is_verified")}),) + auth_admin.UserAdmin.fieldsets
    # fields = ['is_active', 'username', 'name', 'email', 'phone', 'password']
    fieldsets = (
        (None, {
            'fields': ('is_active', 'is_staff', 'username', 'name', 'email', 'phone',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'name', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['username']
    list_display = ["username", "email", "name", "phone",]
    search_fields = ["name", "phone", 'phone', 'username']
    ordering = ["-id"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        override save method to add random username
        In signal it will give a proper username
        """
        obj.username = f"{settings.USERNAME_PREFEX}-{random.randint(0,99)}"
        obj.save()

admin.site.register(User, UserAdmin)
