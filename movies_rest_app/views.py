from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movies_rest_app.models import *
from movies_rest_app.serializers import *


# Create your views here.

@api_view(['GET', 'POST'])
def movies(request):
    if request.method == 'GET':
        movies_qs = Movie.objects.all()
        if 'name' in request.query_params:
            movies_qs = movies_qs.filter(name__iexact=request.query_params['name'])
        if 'duration_from' in request.query_params:
            movies_qs = movies_qs.filter(duration_in_min__gte=request.query_params['duration_from'])
        if 'duration_to' in request.query_params:
            movies_qs = movies_qs.filter(duration_in_min__lte=request.query_params['duration_to'])
        if 'description' in request.query_params:
            movies_qs = movies_qs.filter(description__icontains=request.query_params['description'])
        serializer = MovieSerializer(instance=movies_qs, many=True)
        return Response(serializer.data)
    else:
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            serializer = MovieSerializer(instance=movie, many=False)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def actors(request):
    if request.method == 'GET':
        qs = Actor.objects.all()
        serializer = ActorSerializer(instance=qs, many=True)
        return Response(serializer.data)
    else:
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['Patch', 'DELETE'])
def actor(request, actor_id):
    single_actor = get_object_or_404(Actor, id=actor_id)
    if request.method == 'PATCH':
        serializer = ActorSerializer(instance=single_actor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    else:
        single_actor.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_actors_by_movie(request, movie_id):
    actors_qs = get_object_or_404(Movie, pk=movie_id).movieactor_set.all()
    if "main_role" in request.query_params:
        actors_qs = actors_qs.filter(main_role=request.query_params['main_role'])
    if "salary_from" in request.query_params:
        actors_qs = actors_qs.filter(salary__gte=request.query_params['salary_from'])
    if "salary_to" in request.query_params:
        actors_qs = actors_qs.filter(salary__lte=request.query_params['salary_to'])
    serializer = MovieActorSerializer(instance=actors_qs, many=True)
    return Response(serializer.data)


@api_view(['DELETE', 'PATCH'])
def actor_by_movie(request, movie_id, actor_id):
    actor_from_movie = get_object_or_404(MovieActor, actor_id=actor_id, movie_id=movie_id)
    if request.method == 'DELETE':
        actor_from_movie.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        serializer = MovieActorSerializer(instance=actor_from_movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def oscar(request, movie_id):
    movie_oscars = Oscars.objects.filter(movie_id=movie_id)
    serializer = OscarSerializer(instance=movie_oscars, many=True)
    return Response(serializer.data)



