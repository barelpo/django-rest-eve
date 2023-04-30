from rest_framework import serializers

from movies_rest_app.models import *


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ['actors']
        # depth = 1
        # fields = ['id', 'name', 'release_year']
        # exclude = ['actors', 'description']
        extra_kwargs = {'id': {'read_only': True}, 'actors': {'required': False}}


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}, 'name': {'required': True}, 'birth_year': {'required': True}}


class ActorOscarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ['id', 'name']


class MovieOscarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'name']


class MovieActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieActor
        fields = ['salary', 'main_role', 'actor']
        depth = 1
        extra_kwargs = {'actor': {'read_only': True}, 'movie': {'read_only': True}, 'id': {'read_only': True}}


class OscarMovieActorSerializer(serializers.ModelSerializer):

    movie = MovieOscarSerializer()
    actor = ActorOscarSerializer()

    class Meta:
        model = Oscars
        fields = ['id', 'movie', 'actor', 'year_awarded', 'nomination_type']


class OscarCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Oscars
        fields = '__all__'
        extra_kwargs = {'movie': {'required': True}, 'nomination_type': {'required': True},
                        'year_awarded': {'required': True}, 'actor': {'read_only': True}}


class OscarActorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Oscars
        fields = '__all__'
        extra_kwargs = {'movie': {'required': True}, 'nomination_type': {'required': True},
                        'year_awarded': {'required': True}}



