from django.contrib.auth import get_user_model

from backend.models import Monster

from backend.services import FightRunner


def run(user_id, monster_id):
    user = get_user_model().objects.get(pk=user_id)
    monster = Monster.objects.get(pk=monster_id)

    fr = FightRunner(user, monster)
    fight_result = fr.fight()
    for attack in fight_result:
        print(attack)
