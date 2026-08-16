from django.urls import path
from .views import RedirectURLView

app_name = 'url_shortener'

urlpatterns = [
    path('<str:short_code>/', RedirectURLView.as_view(), name='url-redirect'),
]
