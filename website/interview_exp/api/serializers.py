from rest_framework import serializers

from interview_exp.models import Experiences, Revisions
from user_profile.api.serializers import UserSerializer


class IESerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    verifier = UserSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='experiences_api:ie_detail', lookup_field='id',
                                               lookup_url_kwarg='slug')

    class Meta:
        model = Experiences
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'verifier']


class RevisionSerializer(serializers.ModelSerializer):
    experience = IESerializer()
    reviewer = UserSerializer()

    # experience = serializers.HyperlinkedRelatedField(view_name='experiences_api:ie_detail',
    #                                                  lookup_field='id',
    #                                                  lookup_url_kwarg='slug',
    #                                                  read_only=True)
    # reviewer = serializers.HyperlinkedRelatedField(view_name='user_profile_api:user_detail',
    #                                                lookup_field='username',
    #                                                lookup_url_kwarg='username',
    #                                                read_only=True)
    message = serializers.CharField(required=False)

    class Meta:
        model = Revisions
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id', 'reviewer']
