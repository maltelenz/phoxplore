from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from webxplore.models import Photo, Camera, Manufacturer

@login_required
def index(request):
    all_photos = Photo.objects.all()
    return render_to_response('index.html', {
        'all_photos': all_photos
        })
