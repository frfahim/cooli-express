from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned


class PhoneBackend(ModelBackend):

    def authenticate(self, request, **credentials):
        UserModel = get_user_model()
        phone = credentials.get('phone')
        password = credentials.get('password')
        try:
            user = UserModel.objects.get(phone=phone)
        except (UserModel.DoesNotExist, MultipleObjectsReturned):
            return None
        else:
            if user.check_password(password):
                return user
        return None
