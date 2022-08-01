from pickle import NONE
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import SlugField
from django.utils import timezone
from django.urls import reverse
import uuid



# Create your models here


class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userImage = models.ImageField(default='default.jpeg',upload_to='usersPics')
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    dateJoined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username
    
class Tutor(models.Model):
    idfor = uuid.uuid4
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    tutorId = models.CharField(default=idfor, blank=True,max_length=255)
    
    def __str__(self):
        return self.user.username
    
class Exam(models.Model):  
    idfor = uuid.uuid4
    examiner = models.ForeignKey(Tutor,on_delete=models.CASCADE) #need more thought
    examId = models.CharField(max_length=225,default=idfor)
    title = models.CharField(max_length=2000,unique=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    
    def getId(self):
        return self.examId
    
    def get_absolute_url(self):
        return reverse('setQuestion',kwargs={'examId':self.examId})
    
    def __str__(self):
        return 'examiner:{},title:{}'.format(self.examiner,self.title)

class Question(models.Model):
    idfor = uuid.uuid4
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    questionId = models.CharField(max_length=255,default=idfor)
    question = models.CharField(max_length=2000,unique=False)
    option_a = models.CharField(max_length=2000,blank=False)
    option_b = models.CharField(max_length=2000,blank=False)
    option_c = models.CharField(max_length=2000,blank=True)
    option_d = models.CharField(max_length=2000,blank=True)
    option_e = models.CharField(max_length=2000,blank=True) 
    option_f = models.CharField(max_length=2000,blank=True) 
    answer = models.CharField(max_length=2000)
   
    def __str__(self):
        return str(self.question)
    
    def updateQuestion(self):
        return reverse('updateQuestion',kwargs={
            'questionNumber':self.questionNumber,
            'examId':self.examId
        })
        #INDIVIDUAL EXAM PAPER
class examSheet(models.Model):
    idfor = uuid.uuid4
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exams = models.ForeignKey(Exam,on_delete=models.CASCADE)
    examSheetId = models.CharField(max_length=225,default=idfor)
    dateRegistered = models.DateTimeField(default=timezone.now)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username
    
        #ANSWERS PROVIDED IN AN EXAM
class answeredQuestion(models.Model):
    idfor = uuid.uuid4
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam  = models.ForeignKey(Exam,  on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2000)
    correct = models.BooleanField(default=False)
    wrong = models.BooleanField(default=False)
    
    def __str__(self):
        return self.question.question
        #MARKED  EXAM
class examRecordSheet(models.Model):
    idfor = uuid.uuid4
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.PROTECT)
    totalQuestions = models.IntegerField(null=True)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.student.username
        #TO REQUEST REGISTRATION FOR AN EXAM
class examRequestObject(models.Model):
    idfor = uuid.uuid4
    requestId = models.CharField(max_length=255,default=idfor)
    examId = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
        #link to register for an exam
    def __str__(self):
        return self.user.username
class examRegistrationLink(models.Model):
    examId = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    def __str__(self):
        return self.link
    
