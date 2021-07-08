from django.db import models 
from django.contrib.auth.models import User

from guidelines.models import Subject

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='')
    displayname = models.CharField(default="displayname", max_length=20,)
    #university_scholar = models.CharField(max_length=50, verbose_name="大学")
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")
    #gpa = models.PositiveIntegerField(null=True, blank=True, verbose_name="GPA")
    #toefl_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="托福成绩")
    #gre_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="GRE成绩")

    def __str__(self):
        return '<Profile: %s for %s>' % (self.displayname, self.user.username)

def get_displayname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.displayname
    else:
        return ''

User.get_displayname = get_displayname