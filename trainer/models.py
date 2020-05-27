from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

GENDER_CHOICES = [
    ('1', '女性'),
    ('2', '男性'),
]


class CustomUserManager(UserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Trainer(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=100, verbose_name='姓')
    last_name = models.CharField(max_length=100, verbose_name='名')
    first_read = models.CharField(max_length=100, verbose_name='セイ')
    last_read = models.CharField(max_length=100, verbose_name='メイ')
    gender = models.CharField(max_length=100,
                              verbose_name='性別', choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(
        max_length=254, verbose_name='メールアドレス', unique=True)
    phone = models.CharField(max_length=15, verbose_name='電話番号')
    birth_date = models.DateField(null=True, blank=True, verbose_name='生年月日')
    image = models.ImageField(upload_to='images', verbose_name='画像')
    area = models.CharField(max_length=100)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),
    )

    #date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


@property
def username(self):
    """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
    return self.email
