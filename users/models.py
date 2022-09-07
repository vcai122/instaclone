from django.contrib.auth.models import User
from django.db import models
from PIL import Image

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='', max_length=150, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)

        side_length = min(img.size)
        img = img.crop(((img.width - side_length) // 2, (img.height - side_length) // 2, (img.width + side_length) // 2,
                        (img.height + side_length) // 2))

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(self.pic.path, quality=95)
