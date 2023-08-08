from django.urls import path

from .views import (
    IEListView,
    RetrieveUpdateIEView,
    RevisionsListView,
    RetrieveUpdateRevisionView,
    CreateRevision,
)
from user_profile.views import activate

app_name = 'experiences_api'

urlpatterns = [
    path('', IEListView.as_view(), name='ie_list'),
    path('<int:slug>/', RetrieveUpdateIEView.as_view(), name='ie_detail'),
    path('<int:exp_id>/revisions/<str:review_code>/', CreateRevision.as_view(), name='add_revision'),
    path('revisions/', RevisionsListView.as_view(), name='revision_list'),
    path('revisions/<int:id>/', RetrieveUpdateRevisionView.as_view(), name='revision_detail'),
]
