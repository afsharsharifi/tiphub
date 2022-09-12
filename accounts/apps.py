from django.apps import AppConfig
from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = "حساب های کاربران"


class AccountConfig(AccountConfig):
    AccountConfig.verbose_name = "حساب ها"


class SocialAccountConfig(SocialAccountConfig):
    SocialAccountConfig.verbose_name = "حساب ها در شبکه های اجتماعی"
