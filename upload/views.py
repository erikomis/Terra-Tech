from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os
from django.conf import settings
from django.http import StreamingHttpResponse, Http404



class UploadView(View):
    def get(self, request):
        return render(request, 'index.html')
    

class DownloadView(APIView):

    def get(self, request):
        filename = 'terra-tech.apk'
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        if not os.path.exists(file_path):
            raise Http404('File not found')

        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as fh:
                while True:
                    chunk = fh.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(file_iterator(file_path), content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
     

  

