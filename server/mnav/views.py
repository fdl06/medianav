# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from movies.models import Movie, VideoDirectory

def default(request):
    movies = VideoDirectory.objects.filter(videofile__isnull=False).order_by('-date_added')[:20] 
    return render_to_response('default.html', locals(), context_instance=RequestContext(request))

