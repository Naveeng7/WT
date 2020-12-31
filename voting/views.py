from django.shortcuts import render
from voting.models import positions
from voting.models import candidates
from django.contrib.auth.models import User
from voting.models import voted
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def voting(request):
    pval = None
    ceval = None
    msg = ''
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
            voter = request.POST['voter']
            voter = User.objects.filter(username=voter).first()

            v1 = voted(user=voter, pname=pval)
            yo = v1.save()
            if yo == True:
                candidates.objects.filter(id=ceval.id).update(cvotes=ceval.cvotes + 1)
                msg = f'You have successfully voted { cval } for the posistion { pval }'
            else:
                msg = f'You have already voted for the posistion { pval }'



    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval,
        'msg': msg
    }
    return render(request, 'voting/v_base.html', context)


