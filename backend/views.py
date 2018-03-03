import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView

from backend.models import Monster

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class FightList(ListView):
    template_name = 'backend/fightlist.html'
    extra_context = {
        'title': 'Fight',
    }

    def get_queryset(self):
        return Monster.objects.all()


@method_decorator(login_required, name='dispatch')
class Fight(DetailView):
    model = Monster
    template_name = 'backend/fight.html'
    extra_context = {
        'title': 'Fight',
    }

    def post(self, request, pk):
        monster = self.get_object()
        logger.info('attack %s', monster.name)
        return redirect('fight', pk)


@login_required
def dashboard(request):
    return render(request, 'backend/dashboard.html', {'title': 'Dashboard'})


@method_decorator(login_required, name='dispatch')
class Inventory(ListView):
    template_name = 'backend/inventory.html'
    extra_context = {
        'title': 'Inventory',
    }

    def get_queryset(self):
        return self.request.user.items.all()


@method_decorator(login_required, name='dispatch')
class LevelUp(TemplateView):
    template_name = 'backend/levelup.html'
    extra_context = {
        'title': 'Level up!!!',
    }

    def get(self, request, success=False):
        return super().get(request, didlevel=success)

    def post(self, request):
        logger.info('LevelUp')

        user = request.user
        user.profile.levelup()

        return redirect('levelupview', success=True)
