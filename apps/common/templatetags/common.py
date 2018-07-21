from django.template import Library

register = Library()

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter_function
def get_movie_id(args):
    index = args.index('embed/') + 6
    id = args[index:]
    return id