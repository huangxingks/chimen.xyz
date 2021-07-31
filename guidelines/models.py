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
        verbose_name = '学科'


class University(models.Model):
    name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '大学'


class Guideline(models.Model, VisitNumExpandMethod):

    DEGREE_CHOICES = [
        ('修士', '修士'),
        ('博士', '博士'),
        ('一贯制博士', '一贯制博士'),
    ]

    LANGUAGE_CHOICES = [
        ('日语', '日语'),
        ('英语', '英语'),
    ]

    APPLICATION_METHOD_CHOICES = [
        ('电子邮件', '电子邮件'),
        ('常规邮件', '常规邮件'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")

    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, default='M', verbose_name="学位")

    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='JP', verbose_name="提交方式")

    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="大学")
    school = models.CharField(max_length=50, verbose_name="研究科")
    course = models.CharField(max_length=50, verbose_name="专攻")

    application_available = models.DateTimeField(default=datetime.now(), verbose_name="申请开始日")
    application_deadline = models.DateTimeField(default=datetime.now(), verbose_name="申请结束日")

    application_method = models.CharField(max_length=10, choices=APPLICATION_METHOD_CHOICES, default='Email', verbose_name="申请方式")
    address = models.CharField(null=True, blank=True, max_length=200, verbose_name="常规邮件提交地址")
    email_address = models.EmailField(null=True, blank=True, max_length=100, verbose_name="电子邮件提交地址")

    toefl_required = models.BooleanField(default=False, verbose_name="需要提交托福成绩")
    toefl_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="托福成绩要求")

    gre_required = models.BooleanField(default=False, verbose_name="需要提交GRE成绩")
    gre_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="GRE成绩要求")

    recommendation_letter_required = models.BooleanField(default=False, verbose_name="需要提交推荐信")
    recommendation_letter_num = models.PositiveIntegerField(null=True, blank=True, verbose_name="推荐信数量")

    examination_required = models.BooleanField(default=False, verbose_name="需要笔试")
    examination_date = models.DateTimeField(null=True, blank=True, verbose_name="笔试日期")

    interview_date = models.DateTimeField(null=True, blank=True, verbose_name="面试日期")

    additional_information = RichTextUploadingField(default="暂无补充信息", verbose_name="补充信息")

    def get_url(self):
        return reverse('guidelines:guideline_detail', kwargs={'guideline_pk': self.pk})

    def __str__(self):
        return str(self.university)+str(self.school)+str(self.course)

    class Meta:
        verbose_name = "募集要项"
        ordering = ['subject', 'university', 'school', 'course']
