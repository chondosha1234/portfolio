from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email', 'password'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email, password):
    print("inside pre authenticate in create_session")
    print(email, password)
    user = User.objects.create(email=email, password=password)
    print(user)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
