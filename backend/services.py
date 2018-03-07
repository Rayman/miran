from abc import ABC, abstractmethod
from collections.abc import Iterable
from collections import namedtuple
import random


class Attack(namedtuple('Attack', ['attacker', 'defender', 'damage'])):
    def __str__(self):
        return '%s attacked %s for %d damage' % (self.attacker.name, self.defender.name, self.damage)


class TotalStats(ABC):
    @property
    @abstractmethod
    def min_damage(self):
        pass

    @abstractmethod
    def min_damage(self):
        pass

    @property
    def attack_speed(self):
        return 1.2

    def attack(self, defender):
        dmg = random.randrange(self.min_damage, self.max_damage)
        return Attack(attacker=self, defender=defender, damage=dmg)


class TotalUserStats(TotalStats):
    def __init__(self, user):
        self.user = user

    @property
    def name(self):
        return self.user.username

    @property
    def min_damage(self):
        return 2

    @property
    def max_damage(self):
        return 5

    @property
    def attack_speed(self):
        return 1.2


class TotalMonsterStats(TotalStats):
    def __init__(self, monster):
        self.monster = monster

    @property
    def name(self):
        return self.monster.name

    @property
    def min_damage(self):
        return 2

    @property
    def max_damage(self):
        return 5

    @property
    def attack_speed(self):
        return 1


class FightResult(Iterable):
    def __init__(self):
        self.history = []

    def append(self, attack):
        self.history.append(attack)

    def __iter__(self):
        return iter(self.history)

    def __str__(self):
        return '''Fight result:
        OK
        '''


class FightRunner(object):
    def __init__(self, user, monster):
        self.user = TotalUserStats(user)
        self.monster = TotalMonsterStats(monster)

    def fight(self):
        fr = FightResult()

        user_time = 1 / self.user.attack_speed
        monster_time = 1 / self.monster.attack_speed

        for _ in range(5):
            if user_time <= monster_time:
                attack = self.user.attack(self.monster)
                user_time += 1 / self.user.attack_speed
            else:
                attack = self.monster.attack(self.user)
                monster_time += 1 / self.monster.attack_speed
            fr.append(attack)

        return fr