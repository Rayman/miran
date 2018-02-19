import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


@login_required
def fight(request):
    return render(request, 'backend/fight.html')


@login_required
def dashboard(request):
    return render(request, 'backend/dashboard.html')


@method_decorator(login_required, name='dispatch')
class LevelUp(TemplateView):
    template_name = 'backend/levelup.html'

    def post(self, request):
        logger.info('LevelUp')
        return redirect('levelupview', level=3)
