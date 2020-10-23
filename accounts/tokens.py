from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

from accounts.models import CustomUser


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, date_joined):
        return (
            text_type(user.is_verified)
            + text_type(user.pk)
            + text_type(user.date_joined)
        )


account_activation_token = AccountActivationTokenGenerator()