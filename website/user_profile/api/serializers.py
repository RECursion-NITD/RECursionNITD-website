from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from user_profile.models import Profile
from user_profile.utils import LowerEmailField


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = LowerEmailField(
        required=True,
        allow_blank=False,
        label='Email address',
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match!'})
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'].lower(),
            is_active=False  # TO BE CHANGED TO FALSE
        )
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user_profile_api:user_detail', lookup_field='username',
                                               lookup_url_kwarg='username')

    class Meta:
        model = User
        fields = ['username', 'email', 'url']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.CharField(source='get_role_display', )

    class Meta:
        model = Profile
        exclude = ('id',)
        read_only_fields = ('user', 'role', 'email_confirmed', 'created_at', 'updated_at',)
