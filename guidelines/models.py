from datetime import datetime
from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

from visits.models import VisitNumExpandMethod


class Subject(models.Model):
    name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subject'


class University(models.Model):
    name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'


class Guideline(models.Model, VisitNumExpandMethod):

    DEGREE_CHOICES = [
        ('M', 'Master'),
        ('D.', 'Ph.D.'),
    ]

    LANGUAGE_CHOICES = [
        ('JP', 'Japanese'),
        ('EN', 'English'),
    ]

    APPLICATION_METHOD_CHOICES = [
        ('E', 'Email'),
        ('R', 'Regular mail'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject")

    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, default='M', verbose_name="Degree")

    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='JP', verbose_name="Language")

    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="University")
    school = models.CharField(max_length=50, verbose_name="School")
    course = models.CharField(max_length=50, verbose_name="Course")

    application_available = models.DateTimeField(default=datetime.now(), verbose_name="Application available")
    application_deadline = models.DateTimeField(default=datetime.now(), verbose_name="Application deadline")

    application_method = models.CharField(max_length=10, choices=APPLICATION_METHOD_CHOICES, default='E', verbose_name="Application method")
    address = models.CharField(null=True, blank=True, max_length=200, verbose_name="Address")
    email_address = models.EmailField(null=True, blank=True, max_length=100, verbose_name="Email address")

    toefl_required = models.BooleanField(default=False, verbose_name="TOEFL required")
    toefl_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="TOEFL requirement")

    gre_required = models.BooleanField(default=False, verbose_name="GRE required")
    gre_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="GRE requirement")

    recommendation_letter_required = models.BooleanField(default=False, verbose_name="Recommendation letter required")
    recommendation_letter_num = models.PositiveIntegerField(null=True, blank=True, verbose_name="Recommendation letter number")

    examination_required = models.BooleanField(default=False, verbose_name="Examination required")
    examination_date = models.DateTimeField(null=True, blank=True, verbose_name="Examination date")

    interview_date = models.DateTimeField(null=True, blank=True, verbose_name="Interview date")

    additional_information = RichTextUploadingField(default="No additional information", verbose_name="Additional information")

    def get_url(self):
        return reverse('guidelines:guideline_detail', kwargs={'guideline_pk': self.pk})

    def __str__(self):
        return str(self.university)+str(self.school)+str(self.course)

    class Meta:
        verbose_name = "Guideline"
        ordering = ['subject', 'university', 'school', 'course']
