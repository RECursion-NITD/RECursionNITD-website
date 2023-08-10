from rest_framework import serializers

from team.models import Members


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        exclude = ('id',)
