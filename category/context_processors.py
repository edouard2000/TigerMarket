from .models import Category

def munu_links(request):
    links = Category.objects.all()
    return dict(links = links)