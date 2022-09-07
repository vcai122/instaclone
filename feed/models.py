from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    caption = models.TextField(max_length=2200, blank=True)
    image = models.ImageField(upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['-date_posted']



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=2200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

