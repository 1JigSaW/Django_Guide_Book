from django.shortcuts import render
from django.http import Http404, HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render(request, 'current_datetime.html', locals())

def hours_ahead(request, offset):
    try:
    	offset = int(offset)
    except ValueError:
    	raise Http404()
    dt = datetime. datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>After %s hours will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
