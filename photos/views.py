from django.shortcuts import render

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
# Create your views here.
from .serializers import PhotosSerializer, PhotosListUser
from .models import Photo


class UPLOAD_PHOTO(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser, FileUploadParser,]
    def post(self, request,):
        serializer = PhotosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Delete_Photo(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PhotosSerializer.Meta.model.objects.all()
   

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class List_Photos(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =  PhotosListUser  

    def get_queryset(self):
        user = self.request.user
        return Photo.objects.filter(user=user)

