from django.db import models

class Publisher(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60)
	state_province = models.CharField(max_length=30)
	country = models.CharField(max_length=50)
	website = models.URLField()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Author(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=40)
	email = models.EmailField(blank=True, verbose_name='e-mail')

	def __str__(self):
		return u'%s %s' % (self.first_name, self.last_name)

class DahlManager(models.Manager):
	def get_query_set(self):
		return super(DahlManager, self).get_query_set().filter(
			author='Mikhail Trifonov')

class BookManager(models.Manager):
	def title_count(self, keyword):
		return self.filter(title__icontains=keyword).count()

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,)
	publication_date = models.DateField(blank=True, null=True)
	num_pages = models.IntegerField(blank=True, null=True)
	objects = BookManager()
	dahl_objects = DahlManager()

	def __str__(self):
		return self.title
