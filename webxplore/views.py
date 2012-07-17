from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from webxplore.models import Photo, Camera, Manufacturer

@login_required
def index(request):
    all_photos = Photo.objects.all()
    return render_to_response('index.html', {
        'all_photos': all_photos
        })

@login_required
def photo(request, pk):
    ph = get_object_or_404(Photo, pk = pk)
    return render_to_response('photo.html', {
            'photo': ph
        }
    )
