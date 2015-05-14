from django.conf import settings
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate


def create_intial_superuser(sender, **kwargs):
    """
    create an intial superuser.
    """
    try:
        user, created = User.objects.get_or_create(username='cool')
        user.set_password('cool')
        user.is_superuser = True
        user.is_staff = True
        user.first_name = user.last_name= 'admin'
        user.email = 'cool@example.com'
        user.save()
    except Exception as e:
        pass


class lets_encrypt_demoCoreConfig(AppConfig):
    name = 'lets_encrypt_demo'

    def ready(self, ):
        post_migrate.connect(create_intial_superuser, dispatch_uid="create intial superuser")

