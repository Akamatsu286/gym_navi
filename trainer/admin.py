from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import Trainer


class MyTrainerChangeForm(UserChangeForm):
    class Meta:
        model = Trainer
        fields = '__all__'


class MyTrainerCreationForm(UserCreationForm):
    class Meta:
        model = Trainer
        fields = ('email',)


class MyTrainerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('gender',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyTrainerChangeForm
    add_form = MyTrainerCreationForm
    list_display = ('email', 'first_name', 'last_name', 'gender')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'gender')
    ordering = ('email',)


admin.site.register(Trainer, MyTrainerAdmin)
