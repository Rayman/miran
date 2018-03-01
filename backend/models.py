from enum import unique
import logging

from django.db import models
from django.conf import settings
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import ChoiceEnum


logger = logging.getLogger(__name__)


def exp_to_level(level):
    return 30 + 20 * level


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    level = models.PositiveSmallIntegerField(default=1)
    exp = models.PositiveIntegerField()

    def can_level(self):
        return self.exp > exp_to_level(self.level)

    def levelup(self):
        assert Profile.objects.filter(
            pk=self.pk, exp__gte=exp_to_level(F('level'))).update(
                level=F('level') + 1, exp=F('exp') - exp_to_level(F('level')))

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')

    name = models.CharField(max_length=100)

    TYPES = (
        ('Weapon', (
            (0, 'Dagger'),
            (1, 'Sword'),
            (2, 'Axe'),
        )),
        (3, 'Body'),
    )

    type = models.PositiveIntegerField(choices=TYPES)


class Affix(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='affixes')

    @unique
    class Types(ChoiceEnum):
        local_physical_damage_percent = 0
        local_physical_damage = 1
        local_attack_speed_percent = 2

    type = models.PositiveIntegerField(choices=Types.choices())
    value = models.PositiveIntegerField()


class Monster(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['level']
