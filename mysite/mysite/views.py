from django.shortcuts import render
from django.http import Http404, HttpResponse
import datetime
from books.models import Publisher, Book, Author
from django.views.generic.list import ListView
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control

@vary_on_headers('User-Agent', 'Cookie')
def hello(request):
    return HttpResponse("Hello world")

@cache_control(private=True)
def current_datetime(request):
    current_date = datetime.datetime.now()
    return render(request, 'current_datetime.html', locals())
    
@cache_control(must_revalidate=True, max_age=3600)
def hours_ahead(request, offset):
    try:
    	offset = int(offset)
    except ValueError:
    	raise Http404()
    dt = datetime. datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>After %s hours will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def author_detail(request, author_id):
    response = ListView.object_detail(
        request,
        queryset = Author.objects.all(),
        object_id = author_id,
    )
    now = datetime.datetime.now()
    Author.objects.filter(id=author_id).update(last_accessed=now)
    return response

def books_by_publisher(request, name):
    publisher = get_object_or_404(Publisher, name__iexact=name)
    return ListView.object_list(
        request,
        queryset = Book.objects.filter(publisher=ublisher),
        template_name = 'books_by_publisher.html',
        template_object_name = 'book',
        extra_context = {'publisher': publisher}
    )

def author_list_plaintext(request):
    response = ListView.object_list(
        request,
        queryset = Author.objects.all(),
        mimetype = 'text/plain',
        template_name = 'author_list.txt',
        )
    response["Content-Disposition"] = "attachment; filename=authors.txt"
    return response
# def about_pages(request, page):
#     try:
#         return direct_to_template(request, template='about/%s.html' % page)
#     except TemplateDoesNotExist:
#         raise Http404()
