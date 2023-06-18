from category.models import Category


def menu_links(request):
    """
        Allow to use the links in all the templates
    """
    links = Category.objects.all()
    return dict(links=links)
