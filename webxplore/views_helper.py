from webxplore.models import Photo, Camera, Manufacturer, SourceFolder

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

def get_selection(selection, photos):
    if selection.isdigit():
        return photos.filter(source_folder__id = int(selection))
    return photos

def get_ordered_photos(selection, ordering):
    orderfield = get_order(ordering)

    selection_photos = get_selection(selection, Photo.objects.all()).order_by(orderfield)

    return selection_photos