"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite.views import hello, current_datetime, hours_ahead
from books.views import search_form, search, contact
from books.models import Publisher, Book, Author
from django.views.generic.list import ListView
from mysite.views import author_detail


def get_publishers():
    return Publisher.objects.all()

publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list_pages.html',
    'template_object_name': 'publisher',
    'extra_context': {'publisher_list': Publisher.objects.all()}
}

book_info = {
    'queryset': Book.objects.order_by('-publication_date'),
}

apress_books = {
    'queryset': Book.objects.filter(publisher__name='Apress Publishing'),
    'template_name': 'apress_list.html',
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('time/', current_datetime),
    path('time/plus/<offset>/', hours_ahead),
    path('search-form/', search_form),
    path('search/', search),
    path('contact/', contact),
    path('publishers/', ListView.as_view(), publisher_info),
    path('books/', ListView.as_view(), book_info),
    path(r'authors/(?P<author_id>\d+', author_detail)
    # path('about/', direct_to_template, {
    #     'template': 'about.html'
    #     })
    # path(r'about/(\w+)/', about_pages)
]
