from django.http import Http404, HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>DateTime %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
    	offset = int(offset)
    except ValueError:
    	raise Http404()
    dt = datetime. datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>After %s hours will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
