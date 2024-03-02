from rest_framework import serializers
from .models import Photo


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
    
    def create(self, validated_data):
        photo =  Photo.objects.create(**validated_data)
        return photo
    

class PhotosListUSer(serializers.ModelSerializer) :
    class Meta:
        model = Photo
        fields = ['id', 'image',]
        depth = 1
       

    def list(self, validated_data):
        photo =  Photo.objects.filter(**validated_data)
        return photo
    
    
  

