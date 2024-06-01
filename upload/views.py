from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os
from django.conf import settings
from django.http import HttpResponse, Http404


class UploadView(View):
    def get(self, request):
        return render(request, 'index.html')
    

class DownloadView(APIView):

    def get(self, request, filename, format=None):
        print(filename)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
                return response
        raise Http404('File not found')
     

  

