from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Tutor,
    userProfile,
    Exam,
    examRequestObject,
    Question,
    examSheet,
    examRecordSheet,
    answeredQuestion
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
        

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['user','userImage']
        
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['user','tutorId']
        
class examSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['title','examId']

class examSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = examSheet
        fields = ['student','exams']

class examRequestObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = examRequestObject
        fields = ['user','requestId','examId']
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['exam','questionId','answer']
        
class answeredQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = answeredQuestion
        fields = ['answer']
