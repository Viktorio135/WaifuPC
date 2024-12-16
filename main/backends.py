from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import CustomUser


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Ищем пользователя по email или phone
            user = CustomUser.objects.get(Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        except ValidationError:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None