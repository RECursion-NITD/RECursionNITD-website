from rest_framework import serializers
from getting_started.models import (
    Level,
    Topic,
    SubTopic,
    Note,
    File,
    Link,
)

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ['id','sub_topic']

class TopicSerializer(serializers.ModelSerializer):
    subtopic = SubTopicSerializer(
        source='subtopic_set',
        many=True,
        read_only=True
    )
    class Meta:
        model = Topic
        fields = ['Topic_title','subtopic']

class LevelSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(
        source='topic_set',
        many=True,
        read_only=True
    )
    class Meta:
        model = Level
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    link = LinkSerializer(
        source='link_set',
        many=True,
        read_only=True
    )
    class Meta:
        model = File
        fields = '__all__'


class SubTopicContentSerializer(serializers.ModelSerializer):
    note = NoteSerializer(
        source='note_set',
        many=True,
        read_only=True
    )
    file = FileSerializer(
        source='file_set',
        many=True,
        read_only=True
    )
    class Meta:
        model = SubTopic
        fields = "__all__"





