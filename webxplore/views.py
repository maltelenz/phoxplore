from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext

from webxplore.views_helper import *

@login_required
def index(request):
    (all_photos, ordering) = get_ordered_photos(request)

    possible_orders = possible_orderings()

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
