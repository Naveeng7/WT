from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages

# Create your models here.
class positions(models.Model):
    pname = models.CharField(max_length=25)

    def __str__(self):
        return self.pname

    def save(self, *args, **kwargs):
        pvals = positions.objects.all()
        for p in pvals:
            if self.pname == p.pname:
                return f'Position already exists {p}'
        super(positions, self).save(*args, **kwargs)


class candidates(models.Model):
    pname = models.ForeignKey(positions, on_delete=models.CASCADE)
    cname = models.ForeignKey(User, on_delete=models.CASCADE)
    cvotes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pname,self.cname,self.cvotes}'

    def save(self, *args, **kwargs):
        cvals = candidates.objects.all()
        for c in cvals:
            if c.cname == self.cname and c.pname == self.pname:
                return f'The candidate { self.cname } is already standing for this position { self.pname }'
        super(candidates, self).save(*args, **kwargs)


class voted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pname = models.ForeignKey(positions, on_delete=models.CASCADE)

    def __str__(self):
        return f'{ self.user } votes position { self.pname }'

    def save(self,*args, **kwargs):
        vvals = voted.objects.all()
        for v in vvals:
            if v.user == self.user and v.pname == self.pname:
                #return messages.success(f'You { self.user } have already voted for this position: { self.pname }')
                return f'You { self.user } have already voted for this position: { self.pname }'
        print('vote submitted')
        pval = positions.objects.filter(pname=self.pname).first()
        cval = User.objects.filter(username=self.user).first()
        ceval = candidates.objects.filter(pname=pval, cname=cval).first()
        print(pval,cval,ceval,ceval.id,ceval.cvotes)
        candidates.objects.filter(id=ceval.id).update(cvotes = ceval.cvotes + 1)
        super(voted, self).save(*args, **kwargs)