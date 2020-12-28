from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class positions(models.Model):
    pname = models.CharField(max_length=25)

    def __str__(self):
        return self.pname

class candidates(models.Model):
    pname = models.ForeignKey(positions, on_delete=models.CASCADE)
    cname = models.ForeignKey(User, on_delete=models.CASCADE)
    cvotes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pname,self.cname,self.cvotes}'