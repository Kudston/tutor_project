from venv import create
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User

@receiver(post_save,sender=Exam)
def createExamLink(sender,instance=None,created=False,**kwargs):
    if created:
        newLink = examRegistrationLink.objects.create(examId=instance.examId,link='http://127.0.0.1:8000/request-registration/{}/'.format(instance.examId))
        newLink.save()

@receiver(post_save,sender=examSheet)
def deleteRequestObject(sender,instance=None,created=False,**kwargs):
    if created:
        req_obj = examRequestObject.objects.get(user=instance.student,examId=instance.exams.examId)
        req_obj.delete()

@receiver(post_save,sender=examRecordSheet)
def deleteExamSheet(sender,instance=False,created=False,**kwargs):
    if created:
        sheet = examSheet.objects.get(student=instance.student,exam=instance.exam)
        sheet.delete()