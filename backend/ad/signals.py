from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver
import re
from ad.models import Ad


def to_int(num):
    return int(re.sub(r'\D+', '', num))


@receiver(pre_save, sender=Ad)
def my_handler(sender, **kwargs):
    instance: Ad | None = kwargs.get('instance')
    if not instance:
        return
    current_instance = Ad.objects.filter(pk=instance.pk).first()
    if current_instance:
        if current_instance.price != instance.price:
            instance.need_updates = True
        if current_instance.rating != instance.rating:
            instance.need_updates = True
