from django.shortcuts import render
from voting.models import positions
from voting.models import candidates
from django.contrib.auth.models import User
from voting.models import voted

# Create your views here.
def voting(request):
    pval = None
    ceval = None
    if request.method == 'POST':
        if 'posval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
        if 'canval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['canval']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates.objects.filter(pname=pval, cname=cval).first()

            v1 = voted(user=cval, pname=pval)
            v1.save()



    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval
    }
    return render(request, 'voting/v_base.html', context)


