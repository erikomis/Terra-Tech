from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from auth_api import views
from photos import views as photo_views
from knox.views import LogoutView, LogoutAllView




urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('activate/<str:token>/', views.ActivateAccount.as_view(), name='activate-account'),
    path('forgot-password/', views.forgot_password.as_view()),
    path('verify-token/', views.VerifyToken.as_view()),  
    path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    path('create-user/', views.CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', views.UpdateUserAPI.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),  
    path('logout-all/', LogoutAllView.as_view()),
    path('photos',  photo_views.UPLOAD_PHOTO.as_view()),
    path('photos/<int:pk>',  photo_views.Delete_Photo.as_view()),
    path('photos/', photo_views.List_Photos.as_view()),
    path('photos/filter/', photo_views.Filter_Photos.as_view()),
]
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)