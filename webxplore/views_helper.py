from webxplore.models import Photo, Camera, Manufacturer

def possible_orderings():
    return {
            'date': 'Date taken',
            'path': 'Path',
            'focal': 'Focal length',
        }

def get_order(ordering):
    orderdict = {
        'date': 'taken_date',
        'path': 'path',
        'focal': 'focal_length',
    }

    try:
        orderfield = orderdict[ordering]
    except KeyError:
        orderfield = 'taken_date'
    return orderfield

def get_ordered_photos(ordering):
    orderfield = get_order(ordering)

    all_photos = Photo.objects.all().order_by(orderfield)

    return all_photos