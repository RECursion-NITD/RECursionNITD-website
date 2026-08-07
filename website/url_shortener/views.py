from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShortenedUrl

class RedirectURLView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortenedUrl, short_code=short_code)
        short_url.click_count += 1
        short_url.save(update_fields=['click_count'])
        return Response({'original_url': short_url.original_url}, status=status.HTTP_200_OK)
