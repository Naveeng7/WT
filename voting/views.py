from django.shortcuts import render
from voting.models import positions
from voting.models import candidates

# Create your views here.
def voting(request):
    context = {
        'positions': positions.objects.all(),
        'candidates': candidates.objects.all()
    }
    return render(request, 'voting/v_base.html', context)
