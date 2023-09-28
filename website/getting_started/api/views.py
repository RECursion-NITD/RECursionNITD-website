from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from getting_started.models import Topic, SubTopic, Level
from .serializers import LevelSerializer , SubTopicContentSerializer



class TopicListAPIView(ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def get_queryset(self):
        level = self.request.query_params.get('level', None)
        return super().get_queryset()


class SubTopicRetrieveAPIView(RetrieveUpdateAPIView):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicContentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'subtopic_id'

    def get_queryset(self):
        return super().get_queryset()