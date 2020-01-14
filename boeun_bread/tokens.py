#이메일 관련 토큰 생성
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
#토큰 생성
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.U_is_active)

account_activation_token = AccountActivationTokenGenerator()