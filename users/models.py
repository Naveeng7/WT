from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import Permission

# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    voter_id = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        # cper = User.objects.filter(username=self.user).first()
        # permis = Permission.objects.get(name='Can add post')
        # cper.user_permission.remove(permis)
        super(profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
