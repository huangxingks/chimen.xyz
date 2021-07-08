from django.contrib.contenttypes.models import ContentType

from .models import VisitNum


def visit_once(request, obj):
    content_type = ContentType.objects.get_for_model(obj)
    key = '{}_{}_visited'.format(content_type.model, obj.pk)
    if not request.COOKIES.get(key):
        visit_num, is_created = VisitNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        visit_num.number += 1
        visit_num.save()
    return key