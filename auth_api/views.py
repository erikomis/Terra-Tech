from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser,ForgotPassword
from .serializers import CreateUserSerializerr, UpdateUserSerializer, LoginSerializer,ActivateAccountSerializer, ForgotPasswordSerializer, ValidateTokenSerializer,ResetPasswordSerializer
from knox import views as knox_views
from django.contrib.auth import login
from rest_framework.views import View
from django.shortcuts import render

class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializerr
    permission_classes = (AllowAny, )

   

class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        print(response)
        return Response(response.data, status=status.HTTP_200_OK)
# Create your views here.

class ActivateAccount(View):
    queryset = CustomUser.objects.all()
    serializer_class = ActivateAccountSerializer
    permission_classes = (AllowAny, )

    def get(self, request, token):
        try:
            user = CustomUser.objects.get(token_ativacao=token)
            user.is_active = True
            user.save()
            return render(request, 'conta_ativada.html')
        
        except CustomUser.DoesNotExist:
            return render(request, 'conta_nao_ativada.html')

class forgot_password(CreateAPIView):
    
    queryset = ForgotPassword.objects.all()
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request, format=None):

        data  = request.data
        print(data)
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Token enviado com sucesso'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyToken(CreateAPIView):
   
    serializer_class = ValidateTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        if token is None:
            return Response({'message': 'Token is invalid.'}, status=status.HTTP_404_NOT_FOUND)
        

        return Response({'message': 'Token is valid.'}, status=status.HTTP_200_OK)
    
class ResetPassword(CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny, )

 