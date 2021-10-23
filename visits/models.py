from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions


class VisitNum(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    number = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Vist Number'


class VisitNumExpandMethod():
    def get_visit_num(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            visit_num = VisitNum.objects.get(content_type=content_type, object_id=self.pk)
            return visit_num.number
        except exceptions.ObjectDoesNotExist:
            return 0