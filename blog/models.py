from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse  

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	#find out why does this save() needs *args and **kwargs
	#https://opensource.com/life/15/2/resize-images-python
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		#https://stackoverflow.com/questions/5213025/how-to-check-imagefield-is-empty
		if self.image:
			img = Image.open(self.image.path)

			basewidth = 675
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize), Image.ANTIALIAS)
			img.save(self.image.path)

	#return url as a string with get_absolute
	#find url of the new post 
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})