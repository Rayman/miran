from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def fight(request):
    return render(request, 'backend/fight.html')
