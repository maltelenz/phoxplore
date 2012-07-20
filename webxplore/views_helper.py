from webxplore.models import Photo, Camera, Manufacturer

def possible_orderings():
    return {
            'date': 'Date taken',
            'path': 'Path',
            'focal': 'Focal length',
        }

def get_order(getvariable):
    try:
        ordering = getvariable
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
    return (ordering, orderfield)

def get_ordered_photos(request):
    (ordering, orderfield) = get_order(request.GET['order'])

    all_photos = Photo.objects.all().order_by(orderfield)

    return (all_photos, ordering)