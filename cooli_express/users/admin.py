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
    list_display = ["email", "name", "phone",]
    search_fields = ["name", "phone", 'phone', 'username']
    ordering = ["-id"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

admin.site.register(User, UserAdmin)
