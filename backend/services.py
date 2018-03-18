from abc import ABC, abstractmethod
from collections.abc import Iterable
from collections import namedtuple
from copy import copy
import random


class Attack(namedtuple('Attack', ['attacker', 'defender', 'damage', 'crit'])):
    def __str__(self):
        s = '%s attacked %s for %d damage (%d left)' % (
        self.attacker.name, self.defender.name, self.damage, self.defender.current_life)
        if self.crit:
            return s + ' CRIT!!!'
        else:
            return s


class TotalStats(ABC):
    def __init__(self):
        self.current_life = self.life

    @property
    @abstractmethod
    def level(self) -> int:
        pass

    @property
    def life(self):
        return 38 + 12 * self.level

    @property
    @abstractmethod
    def min_damage(self):
        pass

    @property
    @abstractmethod
    def max_damage(self):
        pass

    @property
    def attack_speed(self):
        return 1.2

    @property
    def crit_chance(self):
        """Change to make a critical hit"""
        return 0.05

    @property
    def crit_damage(self):
        """Damage multiplier of a critical hit"""
        return 1.5

    def attack(self, defender):
        dmg = random.randrange(self.min_damage, self.max_damage)

        crit = random.random() < self.crit_chance
        if crit:
            dmg *= self.crit_damage

        defender.current_life -= dmg
        if defender.current_life < 0:
            defender.current_life = 0
        return Attack(attacker=copy(self), defender=copy(defender), damage=dmg, crit=crit)


class TotalUserStats(TotalStats):
    def __init__(self, user):
        self.user = user
        super().__init__()

    @property
    def name(self):
        return self.user.username

    @property
    def level(self):
        return self.user.profile.level

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
        super().__init__()

    @property
    def name(self):
        return self.monster.name

    @property
    def level(self):
        return self.monster.level

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
        self.winner = None

    def append(self, attack):
        self.history.append(attack)

    def __iter__(self):
        return iter(self.history)

    def __str__(self):
        return '%s won the fight' % self.winner.name


class FightRunner(object):
    def __init__(self, user, monster):
        self.user = TotalUserStats(user)
        self.monster = TotalMonsterStats(monster)

    def fight(self):
        fr = FightResult()

        user_time = 1 / self.user.attack_speed
        monster_time = 1 / self.monster.attack_speed

        while True:
            if user_time <= monster_time:
                attack = self.user.attack(self.monster)
                user_time += 1 / self.user.attack_speed
            else:
                attack = self.monster.attack(self.user)
                monster_time += 1 / self.monster.attack_speed
            fr.append(attack)

            if self.user.current_life <= 0:
                fr.winner = self.monster
                return fr
            elif self.monster.current_life <= 0:
                fr.winner = self.user
                return fr
            else:
                pass  # no winner yet

        return fr