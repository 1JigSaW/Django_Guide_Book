from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from books.models import Book
from django.core.mail import send_mail
from books.forms import ContactForm
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas


UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,
281,304,203, 134, 147]

def search_form(request):
	return render(request, 'search_form.html')

def search(request):
	errors = []
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('Enter your search term.')
		elif len(q) > 20:
			errors.append('Enter up to 20 characters.')
		else:
			books = Book.objects.filter(title__icontains=q)
			return render(request, 'search_results.html', 
				{'books': books, 'query': q})
	return render(request, 'search_form.html', {'errors': errors})

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('e_mail', 'noreply@example.com'),
				['siteowner@example.com'],
			)
			return HttpResponseRedirect('/contact/thanks/')
		else:
			form = ContactForm(initial={'subject': 'I liked your site'})
	return render(request, 'contact_form.html', locals())

def unruly_passengers_csv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename=unruly.csv'
 
    writer = csv.writer(response)
    writer.writerow(['Year','Unruly Airline Passengers'])
    for (year,num) in zip(range(1995,2006), UNRULY_PASSENGERS):
        writer.writerow([year,num])
 
    return response

def hello_pdf(request):
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=hello.pdf'
	p = canvas.Canvas(response)
	p.drawString(100, 100, 'Hello world.')
	p.showPage()
	p.save()
	return response