from django.shortcuts import render
from voting.models import positions
from voting.models import candidates
from django.contrib.auth.models import User
from voting.models import voted
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.
@login_required()
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
            voter = request.POST['voter']
            voter = User.objects.filter(username=voter).first()

            v1 = voted(user=voter, pname=pval)
            yo = v1.save()
            if yo == True:
                candidates.objects.filter(id=ceval.id).update(cvotes=ceval.cvotes + 1)
                messages.info(request, f'You have successfully voted { cval } for the posistion { pval }')
            else:
                messages.info(request, f'You have already voted for the posistion { pval }')

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval
    }
    return render(request, 'voting/v_base.html', context)



@user_passes_test(lambda u: u.is_superuser)
def mpos(request):
    msg = ''
    if request.method == 'POST':
        if 'posval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            pval.delete()
            msg = f'{pval} removed form voting system '
            messages.info(request, f'{pval} removed form voting system ')
        if 'posadd' in request.POST:
            pval = request.POST['posadd']
            pval = pval.capitalize()
            pval = positions(pname=pval)
            msg = pval.save()

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'users': User.objects.all(),
        'msg': msg
    }
    return render(request, 'voting/mpos.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cadd(request):
    msg = ''
    if request.method == 'POST':
        if 'canadd' in request.POST:
            pval = request.POST['canadd']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['candadd']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates(pname=pval, cname=cval)
            msg = ceval.save()

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'users': User.objects.all(),
        'msg': msg
    }
    return render(request, 'voting/cadd.html', context)



@user_passes_test(lambda u: u.is_superuser)
def cdel(request):
    pval = None
    ceval = None
    msg = ''
    if request.method == 'POST':
        if 'candel' in request.POST:
            pval = request.POST['candel']
            pval = positions.objects.filter(pname=pval).first()
        if 'canval' in request.POST:
            pval = request.POST['posval']
            pval = positions.objects.filter(pname=pval).first()
            cval = request.POST['canval']
            cval = User.objects.filter(username=cval).first()
            ceval = candidates.objects.filter(pname=pval, cname=cval).first()
            ceval.delete()
            msg = f'{ cval } is removed from the position { pval }'

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'pval': pval,
        'ceval': ceval,
        'msg': msg
    }

    return render(request, 'voting/cdel.html', context)



@user_passes_test(lambda u: u.is_superuser)
def cres(request):
    canpos = None
    msg = ''
    if request.method == 'POST':
        if 'canpos' in request.POST:
            canpos = request.POST['canpos']
            canpos = positions.objects.filter(pname=canpos).first()

    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'canpos': canpos,
        'msg': msg
    }

    return render(request, 'voting/cres.html', context)