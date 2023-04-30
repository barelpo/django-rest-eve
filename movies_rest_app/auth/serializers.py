from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class CreateUserSerializer(ModelSerializer):

    password = serializers.CharField(max_length=128, validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email', 'username', 'first_name', 'last_name', 'is_staff']
        extra_kwargs = {'email': {'required': True}, 'username': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'],
                                   email=validated_data['email'],
                                   first_name=validated_data.get('first_name', ''),
                                   last_name=validated_data.get('last_name', ''),
                                   is_staff=validated_data.get('is_staff', False)
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user
