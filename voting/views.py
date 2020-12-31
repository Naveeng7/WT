from django.shortcuts import render
from voting.models import positions
from voting.models import candidates
from django.contrib.auth.models import User
from voting.models import voted
from django.contrib.auth.decorators import login_required, user_passes_test

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



@user_passes_test(lambda u: u.is_superuser)
def vadmin(request):
    msg = ''
    if request.method == 'POST':
        if 'posval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            pval.delete()
            msg = f'{pval} removed form voting system '
        if 'posadd' in request.POST:
            pval = request.POST['posadd']
            pval = positions(pname=pval)
            msg = pval.save()
        if 'canadd' in request.POST:
            pval = request.POST['canadd']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['candadd']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates(pname=pval, cname=cval)
            msg = ceval.save()
        if 'candel' in request.POST:
            pval = request.POST['candel']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['canddel']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates.objects.filter(pname=pval, cname=cval).first()
            ceval.delete()
            msg = f'{ cval } is removed from the position { pval }'


    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'users': User.objects.all(),
        'msg': msg
    }
    return render(request, 'voting/vadmin.html', context)