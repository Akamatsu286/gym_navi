from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model

Trainer = get_user_model()


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class TrainerCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = Trainer
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        Trainer.objects.filter(email=email, is_active=False).delete()
        return email


class TrainerUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = Trainer
        fields = ('name', 'read',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = Trainer
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        Trainer.objects.filter(email=email, is_active=False).delete()
        return email
