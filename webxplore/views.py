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

    (all_photos, ordering) = get_ordered_photos(request)

    id_list = list(all_photos.values_list('id', flat = True))

    idx = id_list.index(int(pk))

    try:
        next_id = id_list[idx + 1]
    except IndexError:
        next_id = None

    if idx > 0: #Avoid negative indexing
        try:
            prev_id = id_list[idx - 1]
        except IndexError:
            prev_id = None
    else:
        prev_id = None

    # next = Photo.objects.get(pk = next_id)
    # prev = Photo.objects.get(pk = prev_id)


    return render_to_response('photo.html', {
            'photo': ph,
            'prev_id': prev_id,
            'next_id': next_id,
            'ordering': ordering,
        },
        context_instance = RequestContext(request)
    )
