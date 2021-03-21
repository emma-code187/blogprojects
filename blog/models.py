from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model): 
	title = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	post_image = models.ImageField(default='post.jpg', upload_to='blog_pics')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	featured = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
                                  
		img = Image.open(self.post_image.path)

		if img.width > 640 or img.height > 360:
			output_size = (640, 360)
			img.thumbnail(output_size)
			img.save(self.post_image.path)  


#@receiver(post_save, sender=User)
#def create_user_post(sender, instance, created, **kwargs):
#	if created:
#		Post.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_post(sender, instance, **kwargs):
#	instance.post.save()
		
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return 'Comment {} by {}' .format(self.body, self.name)



