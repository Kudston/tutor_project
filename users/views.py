from email.mime import image
from encodings import utf_8
from multiprocessing import context
from secrets import choice
from tkinter.messagebox import RETRY
from turtle import pos
from urllib import request, response
from urllib.parse import urldefrag
from venv import create
from django import views
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .serializers import UserSerializer,profileSerializer,loginFormSerializer



from .authorization import (
            accessTokenGenerator,
            isAuthenticated_user,
            refreshTokenGenerator,
            decodeAccessToken,
            decodeRefreshToken,
            isAuthenticated_user
)
from .serializers import (
            QuestionSerializer,
            answeredQuestionSerializer,
            examSerializer,
            examSheetSerializer,
            profileSerializer,
            UserSerializer,
            TutorSerializer,
            examRequestObjectsSerializer
)
from .models import *
from .forms import (
    answerCreationForm,
    profileCreationForm,
    questionCreationForm,
    userCreationForm,
    examsCreationForm,
    user_loginForm
)
# Create your views here.
# #sign up
# class signupView(View):
#     def post(self,*args,**kwargs):
#         userform = userCreationForm(self.request.POST)
#         if userform.is_valid():
#             userform.save()
#             image = "http://localhost:8000/images/images/usersPics/IMG_20220412_072823_6862.jpg"
#             newProfile = userProfile(user=User.objects.get(username=self.request.POST['username']))
#             newProfile.save()
#             user = User.objects.get(username=userform.data['username'])
#             data = {
#                 'user':UserSerializer(user).data
#                 }
#             accessToken = accessTokenGenerator(user.id)
#             refreshToken = refreshTokenGenerator(user.id)
#             data['accessToken'] = accessToken
#             r = JsonResponse(data=data)
#             r.set_cookie(key="refreshToken",value=refreshToken)
#             return r
#         else:
#             res =  Response(userform.errors)
#             return  JsonResponse(res.data,safe=False)

@api_view(["POST","GET"])
def signUpView(request):
    if request.method=="POST":
        data = request.data
        if data["password1"]==data["password2"]:
            user_detail = {
                "username":data['username'],
                "email":data["email"],
                "password":data["password2"],
            }
            u_serializer = UserSerializer(data=user_detail)
            if u_serializer.is_valid():
                u_serializer.save()
                user = User.objects.get(username=user_detail['username'])
                image = "http://localhost:8000/images/images/usersPics/IMG_20220412_072823_6862.jpg"
                try:
                    image = data["image"]
                except:
                    pass
                p_details = {
                    "user":user.pk,
                    "userImage":user_image
                }
                p_serializer = profileSerializer(data=p_details)
                if p_serializer.is_valid():
                    p_serializer.save()
                return Response({
                    "username":user_detail['username'],
                    "email":user_detail['email']
                })
            else:
                return Response(u_serializer.errors)
    return Response({
        "userdetail":UserSerializer().data,
        "profiledata":"user_image"           
                    })

##AUTHENTICATION MIXINS CLASS
@api_view(["GET"])
def home(request):
    return Response("hello")
##sign in
class loginView(View):
    def get(self,*args, **kwargs):
        return JsonResponse(loginFormSerializer().data,safe=True)
    def post(self,*args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        # user = authenticate(self.request,username=username,password=password)
        user = User.objects.get(username=username)
        if user is not None:
            login(self.request,user)
            refreshToken = refreshTokenGenerator(user.id)
            data = UserSerializer(user).data
            respond = JsonResponse(data)    
            respond.set_cookie(key="refreshToken",value=refreshToken)
            return respond
        else:
            return HttpResponse("olodo!! dey try remember things,oya enter your correct details")

##profile
class profileView(View):
    
    def get(self,*args, **kwargs):
        if isAuthenticated_user(self.request):
            information = {}
            profile = userProfile.objects.get(user=self.request.user) 
            data1 =  profileSerializer(data=profile) #for non tutor users
            information['data1'] = UserSerializer(profile.user).data
            information['userImage'] = profile.userImage.url
            if profile.is_tutor:
                tutor = Tutor.objects.get(user=self.request.user)
                data2 =  TutorSerializer(data=tutor)  #users_with tutor tag
                information['data2'] = data2.initial_data 
            
            response = Response(information)
            return response 
        else: return JsonResponse('u arent authenticated',safe=False)
           
    def post(self,*args, **kwargs):
        if isAuthenticated_user(request=self.request):
            profile=userProfile.objects.get(user=self.request.user)
            newProfile  = profileCreationForm (self.request.FILES['userImage'],instance=profile)
            if newProfile.is_valid():
                newProfile.save()
                return JsonResponse("successful",safe=False)
            return JsonResponse("my bad!!",safe=False)

#EXAM SECTION
#create exams           
class examsCreationView(View):
    def post(self,*args, **kwargs):
        if isAuthenticated_user(self.request):
            try:
                tutor = Tutor.objects.get(user=self.request.user)
                newExam = Exam.objects.create(examiner=tutor,title=self.request.POST['title'])
                newExam.save()
                link = examRegistrationLink.objects.get(examId=newExam.examId)
                return JsonResponse("you ave created an exam with username {} and your exam registrationLink is {}".format(self.request.POST['title'],link),safe=False)
            except IntegrityError:
                return HttpResponse('an exam with same title exist')
    
#list all exams created
class exams(View):
    def get(self,*args,**kwargs):
        if isAuthenticated_user(self.request):    
            try:
                user = self.request.user
                tutor = Tutor.objects.get(user=user)
                exams = Exam.objects.filter(examiner=tutor)
                data = examSerializer(exams,many=True)
                return JsonResponse(data.data,safe=False)
            except:
                return HttpResponse('you are not a tutor')

#details of exam 
class examDetailView(View):
    def get(self,*args, **kwargs):
        if isAuthenticated_user(self.request):
            examid = self.request.headers['examId']
            exam = Exam.objects.get(examId=examid)
            serialized_exams = examSerializer(exam).data
        
            context = {
                'exam':serialized_exams
            }
            try:
                serialized_request = examRequestObjectsSerializer(examRequestObject.objects.filter(examId=exam.examId),many=True).data
                context['requests']  = serialized_request
            except:
                pass
            try:
                serialized_questions = QuestionSerializer(Question.objects.filter(exam=exam),many=True).data
                context['questions'] = serialized_questions
            except:
                pass
            return JsonResponse(context,safe=False)
    def post(self,*args, **kwargs):
        if isAuthenticated_user(self.request):
            examId = self.request.headers['examId']
            exam = Exam.objects.get(examId=examId)
            examForm = examsCreationForm(self.request.POST,instance=exam)
            if examForm.is_valid():
                examForm.save()
                return HttpResponse('your exams has been updated')
            else:
                return HttpResponse(examForm.errors)
#request exams registration
class requestRegistrationView(View):
    def post(self, *args, **kwargs):
        examId = kwargs['examId']
        examrequest,created = examRequestObject.objects.get_or_create(user=self.request.user,examId=examId)
        if not created:
            return HttpResponse("you ave already sent a request")
        return HttpResponse("your request has been sent successfully")
        
#acceptRegistration
class acceptRegistrationView(View):
    def get(self,*args, **kwargs):
        examId = self.request.headers['examid']
        requestObjects  = examRequestObject.objects.filter(examId=examId)
        requests = examRequestObjectsSerializer(requestObjects,many=True)
        return JsonResponse(requests.data,safe=False)
    def post(self,*args, **kwargs):
        data = self.request.POST
        requestId  = data['requestId']
        if data['choice']=='accept':
            try:
                requested = examRequestObject.objects.get(requestId=requestId)
                exam = Exam.objects.get(examId = requested.examId)
                examsheet,created = examSheet.objects.get_or_create(student=requested.user,exams=exam)
                if  created:
                    examsheet.save()
                    return HttpResponse('you just accepted {} as a student for your exam'.format(requested.user.username))
                
                return HttpResponse('student already registered')
            except:
                return HttpResponse('requestId does not exist anymore')
        elif data['choice']=='reject':
            try:
                requested = examRequestObject.objects.get(requestId=requestId)
                requested.delete()
            except:
                return HttpResponse('invalid params provided')
    
#exam questions
class setQuestionView(View):
    def post(self,*args, **kwargs):
        examId = self.request.headers['examid']
        exam = Exam.objects.get(examId=examId)
        form = questionCreationForm(self.request.POST)#question,option_a,option_b are important
        if form.is_valid():
            form.instance.exam = exam
            form.save()
            return HttpResponse('your question have been created')
        else:
            return HttpResponse('provide values for the following fields {}'.format(form.errors))
class questionsView(View):
    def get(self,*args, **kwargs):
        examId = self.request.headers['examid']
        exam = Exam.objects.get(examId=examId)
        questions  = Question.objects.filter(exam=exam)
        serialized = QuestionSerializer(questions,many=True)
        return JsonResponse(serialized.data,safe=False)
class questionDetailView(View):
    def get(self,*args, **kwargs):
        questionId = self.request.headers['questionId']
        question = Question.objects.get(questionId=questionId)
        serialized  = QuestionSerializer(question).data
        answer = question.answer
        context = {
            'question':serialized,
            'answer':answer
            
        }
        return JsonResponse(context,safe=False)
    def post(self,*args, **kwargs):
        questionId = self.request.headers['questionId']
        question = Question.objects.get(questionId=questionId)
        questionForm = questionCreationForm(self.request.POST,instance=question)
        if questionForm.is_valid():
            questionForm.save()
            return HttpResponse('your question has been updated successfully')
        else:
            return HttpResponse('invalid update parameters provided')


##taking exams sections
class registeredExamView(View):
    def get(self,*args, **kwargs):
        exams = examSheet.objects.filter(student=self.request.user)
        serialized_exams = examSheetSerializer(exams,many=True).data
        return JsonResponse(serialized_exams,safe=False)

    def post(self,*args, **kwargs):
        exam = Exam.objects.get(examId=self.request.POST['examId'])
        sheet = examSheet.objects.get(student=self.request.user,exams=exam)
        examTitle = sheet.exams.title
        context = {
            'title':examTitle,
            'sheetId':sheet.examSheetId
        }        
        return JsonResponse(context)
class getQuestionView(View):
    def post(self,*args, **kwargs):
        data = self.request.POST
        sheet = examSheet.objects.get(examSheetId=data['sheetId'])
        exam = sheet.exams
        question = Question.objects.filter(exam=exam)[int(data['question_number'])]
        serialized_question = QuestionSerializer(question).data
        context = {
            'question':question,
        }
        try:
            answered = answeredQuestion.objects.get(student=self.request.user,question=question)
            serialized_answer = answeredQuestionSerializer(answered).data
            context['answer'] = serialized_answer
        except:
            pass
        return JsonResponse(context)
class submitAnswersView(View):
    def post(self,*args, **kwargs):
        headers = self.request.headers
        post_data = self.request.POST
        question = Question.objects.get(questionId=headers['questionId'])
        answer = post_data['answer']
        correct = False
        wrong = True
        if len(answer)>0:
            if option+"{}".format(answer) == question.answer:
                correct = True
                wrong = False
        filled_form = {
            'student':self.request.user,
            'exam':question.exam,
            'question':question,
            'answer':answer,
            'correct':correct,
            'wrong':wrong            
        }
        try:
            answered = answeredQuestion.objects.get(question=question,student=self.request.user)
            newAnswer = answerCreationForm(filled_form,instance=answered)
            newAnswer.save()
            return HttpResponse()
        except:
            newAnswer = answerCreationForm(filled_form,instance=answered)
            newAnswer.save()
            return HttpResponse("submitted") 
        
class submitExamView(View):
    def post(self,*args, **kwargs):
        data  = self.request.POST
        student = self.request.user
        exam = Exam.objects.get(examId = data['examId'])
        answered_questions  = answeredQuestion.objects.filter(exam=exam,student=student)
        corrects = 0
        for answered in answered_questions:
            if answered.correct:
                score += 1
        score = corrects
        total_questions = len(answered_questions)
        newRecord = examRecordSheet.objects.create(student=student,exam=exam,totalQuestions=total_questions,score=score)
        newRecord.save()

    