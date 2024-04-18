from rest_framework import serializers
from .models import CustomUser, ForgotPassword
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', )


class CreateUserSerializerr(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def send_email(self, user):
        try:
            subject = 'Ative sua conta'
            message = f'Hi {user.first_name},\n\nWelcome to our site. We are glad to have you here.'
            email_from = 'suport@www.projetos-web.com'
            recipient_list = [user.email]  # Passando o email como uma lista
            html_content = f'Olá {user.first_name},\n\nPara ativar sua conta, clique no link a seguir:\n\n{settings.FRONTEND_URL}/activate/{user.token_ativacao}/'

            email = send_mail(subject, message, email_from, recipient_list, html_message=html_content)
            email.send()
            
        except Exception as e:
            print(e)    





    def create(self, validated_data):
        token_ativacao = get_random_string(32)
        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
            token_ativacao=token_ativacao
        )
        self.send_email(user)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')
        print(email)
        print(password)

        if not email or not password:
            raise serializers.ValidationError("Please give both email or password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)

        if not user:
            raise serializers.ValidationError("Wrong Credentials.")
        print(user)
        attrs['user'] = user
        return attrs
    
class ActivateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('token_ativacao', )
        extra_kwargs = { 'token_ativacao': {'required': True} }


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = ForgotPassword
        fields = ['email']

    def create(self, validated_data):
        email = validated_data.get('email')
        token = get_random_string(length=6, allowed_chars='1234567890')
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Este email não está registrado ou email invalido.")

        forgot_password = ForgotPassword.objects.create(user=user, token=token)
        self.send_email(user, token)
        return forgot_password
  

    def send_email(self, user, token):
        try:
            print(user)
            subject = 'Esqueceu a senha'
            message = f'Olá {user.first_name},\n\nPara redefinir sua senha, você pode usar o seguinte codigo: {token}.\n\nSe você não solicitou a redefinição da senha, ignore este email.'
            email_from = 'suport@www.projetos-web.com'
            recipient_list = [user.email]  # Passando o email como uma lista
            html_content = f'Olá {user.first_name},\n\nPara redefinir sua senha, você pode usar o seguinte codigo: {token}.\n\nSe você não solicitou a redefinição da senha, ignore este email.'

            email = send_mail(subject, message, email_from, recipient_list, html_message=html_content)
            email.send()
            
        except Exception as e:
            print(e)  


class ValidateTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if ForgotPassword.objects.filter(token=value).exists():
            return value
        raise serializers.ValidationError('Token is invalid.')

    def validate(self, data):
        token = data.get('token')
        if token and ForgotPassword.objects.filter(token=token).exists():
            return data
        raise serializers.ValidationError('Token is invalid.')
        
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        password = data.get('password')
        if token and password:
            if ForgotPassword.objects.filter(token=token).exists():
                return data
        raise serializers.ValidationError('Token is invalid.')

    def save(self, **kwargs):
        token = self.validated_data.get('token')
        password = self.validated_data.get('password')
        forgot_password = ForgotPassword.objects.get(token=token)
        user = forgot_password.user
        user.set_password(password)
        user.save()
        forgot_password.delete()
        return user