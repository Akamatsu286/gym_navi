from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, TrainerCreateForm, TrainerUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)

Trainer = get_user_model()


class Top(generic.TemplateView):
    template_name = 'trainer/top.html'


class Trainer_login(LoginView):
    form_class = LoginForm
    template_name = 'trainer/trainer_login.html'


class Trainer_logout(LogoutView):
    template_name = 'trainer/top.html'


class TrainerCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'trainer/trainer_create.html'
    form_class = TrainerCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string(
            'trainer/mail_template/create/subject.txt', context)
        message = render_to_string(
            'trainer/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('trainer:trainer_create_done')


class TrainerCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'trainer/trainer_create_done.html'


class TrainerCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'trainer/trainer_create_complete.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                trainer = Trainer.objects.get(pk=user_pk)
            except Trainer.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not trainer.is_active:
                    # 問題なければ本登録とする
                    trainer.is_active = True
                    trainer.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class TrainerDetail(OnlyYouMixin, generic.DetailView):
    model = Trainer
    template_name = 'trainer/trainer_detail.html'


class TrainerUpdate(OnlyYouMixin, generic.UpdateView):
    model = Trainer
    form_class = TrainerUpdateForm
    template_name = 'trainer/trainer_form.html'

    def get_success_url(self):
        return resolve_url('trainer:trainer_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('trainer:password_change_done')
    template_name = 'trainer/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'trainer/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'trainer/mail_template/password_reset/subject.txt'
    email_template_name = 'trainer/mail_template/password_reset/message.txt'
    template_name = 'trainer/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('trainer:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'trainer/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('trainer:password_reset_complete')
    template_name = 'trainer/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'trainer/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'trainer/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string(
            'trainer/mail_template/email_change/subject.txt', context)
        message = render_to_string(
            'trainer/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('trainer:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'trainer/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'trainer/email_change_complete.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            Trainer.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)
