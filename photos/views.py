from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
# Create your views here.
from .serializers import PhotosSerializer, PhotosListUser, PhotosCountThereDisease
from .models import Photo
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta


def parse_month_param(month_param):
    try:
        month = int(month_param)
        if 1 <= month <= 12:
            return datetime(datetime.now().year, month, 1)
    except ValueError:
        pass
    return None

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


class Filter_Photos(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotosCountThereDisease
    pagination_class = None

    def get(self, request):
        month_param = request.query_params.get('month')
        user = request.user
        if month_param is not None:
        # Verificar se o parâmetro de mês foi fornecido e parsear para um objeto de data
            month_date = parse_month_param(month_param)
            if not month_date:
                return Response({'error': 'Parâmetro de mês inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            first_day = month_date.replace(day=1)
            last_day = (month_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Último dia do mês

            queryset_true = Photo.objects.filter(user=user, there_disease=True, created_at__range=(first_day, last_day))
            queryset_false = Photo.objects.filter(user=user, there_disease=False, created_at__range=(first_day, last_day))

            true_disease = queryset_true.count()
            false_disease = queryset_false.count()

            return Response({'true_disease': true_disease, 'false_disease': false_disease}, status=status.HTTP_200_OK)
        else:
            queryset_true = Photo.objects.filter(user=user, there_disease=True)
            queryset_false = Photo.objects.filter(user=user, there_disease=False)

            true_disease = queryset_true.count()
            false_disease = queryset_false.count()

            return Response({'true_disease': true_disease, 'false_disease': false_disease}, status=status.HTTP_200_OK)
    
