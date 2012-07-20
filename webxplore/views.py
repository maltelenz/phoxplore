from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext

from webxplore.models import Photo, Camera, Manufacturer

@login_required
def index(request):
    try:
        ordering = request.GET['order']
    except KeyError:
        ordering = 'date'

    orderdict = {
        'date': 'taken_date',
        'path': 'path',
        'focal': 'focal_length',
    }

    try:
        orderfield = orderdict[ordering]
    except KeyError:
        orderfield = 'taken_date'
        ordering = 'date'

    all_photos = Photo.objects.all().order_by(orderfield)

    possible_orders = {
        'date': 'Date taken',
        'path': 'Path',
        'focal': 'Focal length',
    }

    return render_to_response('index.html', {
        'all_photos': all_photos,
        'ordering': ordering,
        'possible_orders': possible_orders,
        },
        context_instance = RequestContext(request)
    )

@login_required
def photo(request, pk):
    ph = get_object_or_404(Photo, pk = pk)
    return render_to_response('photo.html', {
            'photo': ph,
        },
        context_instance = RequestContext(request)
    )
