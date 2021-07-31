from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags

from notifications.signals import notify

from .models import Comment


@receiver(post_save, sender=Comment)
def send_notifications(sender, instance, **kwargs):
    """
    if instance.recipient is None:
        
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'guideline':
            guideline = instance.content_object
            verb = '{0} commented your {1}'.format(instance.user.get_displayname(), guideline)
        else:
            raise Exception('unkown object type')
    else:
    """
    if True:
        recipient = instance.recipient
        verb = '{0} commented your {1}'.format(instance.user.get_displayname(), strip_tags(instance.parent.text))
        url = instance.content_object.get_url() + "#comment-" + str(instance.pk)
        notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)
