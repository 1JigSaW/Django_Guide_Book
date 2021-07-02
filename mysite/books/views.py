from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from books.models import Book
from django.core.mail import send_mail
from books.forms import ContactForm

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