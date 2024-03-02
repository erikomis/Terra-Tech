from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives, send_mail


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
            subject, from_email, to = 'Welcome to our site',   'suport12@projetos-web.com', 'suport@projetos-web.com'
            text_content = 'This is an important message.'
            html_content = f'<p>Hi {user.first_name}, welcome to our site. We are glad to have you.</p>'
            msg = send_mail(subject, text_content, from_email, [to], html_message=html_content)
        except Exception as e:
            print(e)





    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
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
            raise serializers.ValidationError("Please give both email and password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)

        if not user:
            raise serializers.ValidationError("Wrong Credentials.")
        print(user)
        attrs['user'] = user
        return attrs