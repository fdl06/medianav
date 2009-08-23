from django.db import models

# Create your models here.

class MovieStatus(models.Model):
    """ Things like Owned, Wish List """
    name = models.CharField(max_length=16, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=16, blank=True)
    
    def __unicode__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=32, blank=True)
    
    def __unicode__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=256, blank=True)
    imdb_id = models.CharField(max_length=32, blank=True)
    
    def __unicode__(self):
        return self.name

class Cast(models.Model):
    person = models.ForeignKey(Person, related_name='cast_person')
    movie = models.ForeignKey('Movie', related_name='cast_movie')
    role = models.CharField(max_length=1024, blank=True)
    job = models.CharField(max_length=64, blank=True)
    bill_order = models.IntegerField(blank=True, null=True) # Order as it appears in imdb
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.person.name, self.movie.title, self.job)

class Company(models.Model):
    name = models.CharField(max_length=256, blank=True)
    imdb_id = models.CharField(max_length=32, blank=True)
    
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=256, blank=True)
    
    def __unicode__(self):
        return self.name

class Movie(models.Model):
    # This model is based on the imdb model from imdbpy
    title = models.CharField(max_length=256)
    imdb_id = models.CharField(max_length=16, blank=True)
    imdb_last_updated = models.DateTimeField(blank=True, null=True)
    imdb_long_title = models.CharField(max_length=256, blank=True)
    canon_title = models.CharField(max_length=256, blank=True)
    imdb_canon_long_title = models.CharField(max_length=256, blank=True)
    year = models.IntegerField(blank=True, null=True)
    imdb_kind = models.CharField(max_length=16, blank=True) # One of movie, tv series, tv mini series, video game, video movie, tv movie, episode
    imdb_index = models.CharField(max_length=16, blank=True) # roman number for movies with the same title/year
   
    cast = models.ManyToManyField(Person, through='Cast') # The cast contains directors, writers and actors
    imdb_cover_url = models.URLField(verify_exists=False, blank=True)
    plot = models.CharField(max_length=4096, blank=True)
    plot_outline = models.CharField(max_length=4096, blank=True)
    imdb_rating = models.FloatField(blank=True, null=True)
    imdb_votes = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    countries = models.ManyToManyField(Country)
    genres = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    certificates = models.ManyToManyField(Certificate)
    mpaa = models.CharField(max_length=128, blank=True)
    production_companies = models.ManyToManyField(Company)

    status = models.ForeignKey(MovieStatus, blank=True, null=True)
    watched = models.DateTimeField(blank=True, null=True)

    #overview = models.CharField(max_length=4096, blank=True)
    #release = models.DateField(blank=True, null=True)
    trailer_url = models.URLField(verify_exists=False, blank=True)
    #homepage = models.URLField(verify_exists=False, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)
    moviedb_rating = models.FloatField(blank=True, null=True)
    moviedb_url = models.URLField(verify_exists=False, blank=True)
    moviedb_poster_url = models.URLField(verify_exists=False, blank=True)
    moviedb_backdrop_url = models.URLField(verify_exists=False, blank=True)
    moviedb_last_updated = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.name


class VideoFormat(models.Model):
    name = models.CharField(max_length=32)

class VideoDirectory(models.Model):
    """ Assumes one movie per directory """
    name = models.CharField(max_length=1024, blank=True)
    format = models.ForeignKey(VideoFormat, blank=True, null=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True)

class VideoFile(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)
    directory = models.ForeignKey(VideoDirectory, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    size = models.Field(blank=True, null=True)

