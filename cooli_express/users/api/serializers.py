from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, exceptions
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from cooli_express.customers.models import Customer, PaymentInfo


User = get_user_model()


class AuthUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["uuid", "username", "phone", "email", "name", "is_verified"]


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["uuid", "username", "phone", "email", "name", "is_verified"]


class RegisterSerializer(BaseRegisterSerializer):
    username = serializers.CharField(required=False)
    phone = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Duplicate phone number")]
    )
    name = serializers.CharField()
    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'name': self.validated_data.get('name', ''),
        }

    @staticmethod
    def generate_username(user):
        # user = User.objects.last()
        base_name = settings.USERNAME_PREFEX
        base_number = 1
        if user and user.username:
            base_number = user.username.strip(base_name)
            if base_number.isdigit():
                base_number = int(base_number)
            else:
                base_number = int(user.id)
        if user and user.id:
            base_number = user.id
        username = base_name + f"{base_number:05d}"
        return username

    def custom_signup(self, request, user):
        data = self.cleaned_data
        user.phone = data.get('phone')
        user.name = data.get('name')
        # user.username = self.generate_username()
        user.save()

    def create_customer(self, user):
        Customer.objects.create(
            user=user,
            email=user.email,
            phone=user.phone,
        )

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        # commit false so user will not save here
        adapter.save_user(request, user, self, commit=False)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        # TODO change this only for customer
        # self.create_customer(user)
        return user


class ExtendedRegisterSerializer(RegisterSerializer):

    def create_customer(self, user, customer_data):
        return Customer.objects.create(
            user=user,
            email=user.email,
            **customer_data,
        )

    def create_payment(self, customer, payment_data):
        PaymentInfo.objects.create(
            customer=customer,
            **payment_data,
        )

    @transaction.atomic
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        customer = request.data.pop('customer')
        payment = request.data.pop('payment')
        self.cleaned_data = self.get_cleaned_data()
        # commit false so user will not save here
        adapter.save_user(request, user, self, commit=False)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        customer = self.create_customer(user, customer)
        self.create_payment(customer, payment)
        return user


class LoginSerializer(BaseLoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    # def authenticate(self, **kwargs):
    #     return authenticate(self.context['request'], **kwargs)

    def _validate_username_email_phone(self, username, email, phone, password):
        user = None

        if not user:
            user = self.authenticate(email=username, password=password)
        if not user:
            user = self.authenticate(username=username, password=password)
        if not user:
            user = self.authenticate(phone=username, password=password)
        if not user:
            msg = _('Must include either "username" or "email" or "phone and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = self._validate_username_email_phone(username, email, phone, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['username'] = user.username
        token['email'] = user.email

        return token
