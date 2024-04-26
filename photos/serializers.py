from rest_framework import serializers
from .models import Photo
from .analysis import Analysis
from auth_api.models import CustomUser as User
import os

class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'user'] 
    
    def create(self, validated_data):
        image = validated_data.pop('image')
        photo = Photo.objects.create(image=image, user=validated_data['user'])
    

        script_dir = os.path.dirname(__file__)  # Obtém o diretório do script atual
        model_path = os.path.join(script_dir, 'model.pkl')  # Cria o caminho absoluto para model.pkl
        analysis_result = Analysis(photo.image.path, model_path).predict()

        print (analysis_result)

        if analysis_result is not None:
            if analysis_result[0] == 1:
               photo.there_disease = True
            else:
                photo.there_disease = False

        photo.save()
        print(photo.there_disease)
        return photo
    

class UserPhotosSerializer(serializers.ModelSerializer):
    class Meta:
            model = User 
            fields = ['id', 'email', ]

class PhotosListUser(serializers.ModelSerializer) :
    user = UserPhotosSerializer()  
    class Meta:
        model = Photo
        fields = ['id', 'image','there_disease','user']
        depth = 1
       

    def list(self, validated_data):
        Photo = Photo.objects.filter(user=validated_data['user'])
        return Photo
    
    
    
  

