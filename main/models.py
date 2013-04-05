# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Course(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'Название курса')
    short_summary = models.TextField(blank=True, null=True, max_length=200, verbose_name=u'Краткое описание курса', help_text=u'Не более 200 символов')
    description = models.TextField(blank=True, null=True, verbose_name=u'Подробное описание курса')
    organisation = models.CharField(blank=True, null=True, max_length=30, verbose_name=u'Название организации')
    logo = models.FileField(blank=True, null=True, upload_to='logos', verbose_name=u'Логотип')
    start_date = models.DateField(blank=True, null=True, verbose_name=u'Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name=u'Дата окончания')
    author = models.ForeignKey(User, verbose_name=u'Создатель курса')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата создания')
    admin_summary = models.TextField(verbose_name=u'Заявка на создание курса', help_text=u'Опишите курс, который Вы желаете разместить')
    approved = models.BooleanField(verbose_name=u'Подтверждение')
    available = models.BooleanField(verbose_name=u'Размещение')

    def __repr__(self):
        return "%s %s" % (self.name, str(self.start_date))
    def __unicode__(self):
        return unicode("%s %s" % (self.name, str(self.start_date)))

class Material(models.Model):
    name = models.CharField(blank=True, max_length=100, verbose_name=u'Название')
    date = models.DateTimeField(verbose_name=u'Дата создания')
    appear_date = models.DateTimeField(verbose_name=u'Дата размещения')
    author = models.ForeignKey(User, verbose_name=u'Автор')
    course = models.ForeignKey(Course, verbose_name=u'Курс')

    def __repr__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class Video(models.Model):
    material = models.ForeignKey(Material, verbose_name=u'Материал')
    youtube_video_id = models.CharField(max_length=32, verbose_name=u'YouTube video ID')

    def __repr__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class Document(models.Model):
    material = models.ForeignKey(Material, verbose_name=u'Материал')
    doc = models.FileField(upload_to='docs', verbose_name=u'Файл')

    def __repr__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class Information(models.Model):
    material = models.ForeignKey(Material, verbose_name=u'Материал')
    text = models.TextField(verbose_name=u'Текст')

    def __repr__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class Feedback(models.Model):
    body = models.TextField(verbose_name=u'Текст сообщения')

    def __repr__(self):
        return self.body
    def __unicode__(self):
        return unicode(self.body)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    courses = models.ManyToManyField(Course, blank=True)

    def is_student(self):
        return True if (len(self.user.groups.filter(name='students')) > 0) else False

    def is_instructor(self):
        return True if (len(self.user.groups.filter(name='instructors')) > 0) else False

    def __repr__(self):
        return str(self.user)
    def __unicode__(self):
        return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
