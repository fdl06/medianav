# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from movies.models import *
from django.db.models import Count
import datetime

def search(request):
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        movies = Movie.objects.filter(title__icontains=query)
        people = Person.objects.filter(name__icontains=query).annotate(num_movies=Count('movie')).order_by('-num_movies')
    else:
        query = 'No search criteria specified' 
    return render_to_response('search_result.html', locals(), context_instance=RequestContext(request))

def movies_list(request):
    movies = Movie.objects.all()
    return render_to_response('movies_list.html', locals(), context_instance=RequestContext(request))

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    directors = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='director').order_by('bill_order')
    actors = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='actor').order_by('bill_order')
    writers = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='writer').order_by('bill_order')
    return render_to_response('movie_detail.html', locals(), context_instance=RequestContext(request))

def genre_detail(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    movies = genre.movie_set.all()
    return render_to_response('genre_detail.html', locals(), context_instance=RequestContext(request))

def person_detail(request, person_id):
    person = Person.objects.get(pk=person_id)
    cast = Cast.objects.filter(person__id=person_id).order_by('-movie__year')
    return render_to_response('person_detail.html', locals(), context_instance=RequestContext(request))

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    movies = company.movie_set.all().order_by('-year')
    return render_to_response('company_detail.html', locals(), context_instance=RequestContext(request))

def country_detail(request, country_id):
    country = Country.objects.get(pk=country_id)
    movies = country.movie_set.all()
    return render_to_response('country_detail.html', locals(), context_instance=RequestContext(request))

def json_movies_list(request):
    """ Returns a list of movies in json """
    movies = Movie.objects.all()
    return HttpResponse(serializers.serialize('json', movies, fields=('title', 'year', 'moviedb_id', 'genres')), content_type='application/json')

def json_genre_list(request):
    """ Returns a list of genres in json """
    genres = Genre.objects.all()
    return HttpResponse(serializers.serialize('json', genres, fields=('name')), content_type='application/json')

def json_movie_directories(request, movie_id):
    """ Returns a json result with a list of directories for a movie """
    directories = VideoDirectory.objects.filter(movie__id=movie_id)
    return HttpResponse(serializers.serialize('json', directories, fields=('name')), content_type='application/json')

def json_directory_videofiles(request, directory_id):
    """ Returns a json result with a list of episodes for a particular show """
    videofiles = VideoFile.objects.filter(directory__id=directory_id)
    return HttpResponse(serializers.serialize('json', videofiles, fields=('name')), content_type='application/json')

def json_movie_detail(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    return HttpResponse(serializers.serialize('json', movie),  content_type='application/json')
