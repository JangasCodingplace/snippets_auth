from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class UserConfig(AppConfig):
    name = 'User'
    verbose_name = _('User')

    def ready(self):
        import User.User
