from django.shortcuts import render
from voting.models import positions
from voting.models import candidates

# Create your views here.
def voting(request):
    if request.method == 'POST':
        val = request.POST['drop1']
        val = positions.objects.filter(pname=val).first()
    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all(),
        'val': val
    }
    return render(request, 'voting/v_base.html', context)


