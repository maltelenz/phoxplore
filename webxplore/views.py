from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from webxplore.views_helper import *

@login_required
def index(request, ordering, page):
    all_photos = get_ordered_photos(ordering)

    paginator = Paginator(all_photos, 25)

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    possible_orders = possible_orderings()

    try:
        page_i = int(page)
    except TypeError:
        #no page given
        page_i = 1

    pagination_range = [i for i in paginator.page_range if i in (
        range(page_i - 2, page_i + 2) + [1] + [paginator.num_pages]
    )]

    return render_to_response('index.html', {
        'photos': photos,
        'all_photos': all_photos,
        'ordering': ordering,
        'possible_orders': possible_orders,
        'pagination_range': pagination_range,
        },
        context_instance = RequestContext(request)
    )

@login_required
def photo(request, pk, ordering):
    ph = get_object_or_404(Photo, pk = pk)

    all_photos = get_ordered_photos(ordering)

    id_list = list(all_photos.values_list('id', flat = True))

    idx = id_list.index(int(pk))

    total = len(id_list)
    nrprev = idx
    nrnext = total - idx - 1

    first_id = id_list[0]
    last_id = id_list[-1]

    next = None
    try:
        next_id = id_list[idx + 1]
        next = Photo.objects.get(pk = next_id)
    except IndexError:
        next_id = None

    prev = None
    if idx > 0: #Avoid negative indexing
        try:
            prev_id = id_list[idx - 1]
            prev = Photo.objects.get(pk = prev_id)
        except IndexError:
            prev_id = None
    else:
        prev_id = None



    return render_to_response('photo.html', {
            'photo': ph,
            'prev_id': prev_id,
            'next_id': next_id,
            'first_id': first_id,
            'last_id': last_id,
            'next': next,
            'prev': prev,
            'ordering': ordering,
            'nrnext': nrnext,
            'nrprev': nrprev,
        },
        context_instance = RequestContext(request)
    )
