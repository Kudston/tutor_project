from atexit import register
from pickle import TRUE
from re import template
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/',views.signupView.as_view(),name='signup'),    
    path('signin/',views.loginView.as_view(),name='signin'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password-reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<token>/<uidb64>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('profile/',views.profileView.as_view(),name='profile'),
    path('create-exam/',views.examsCreationView.as_view(),name='createExam'),
    path('created-exams/',views.exams.as_view(),name='created_exams'),
    ##exam detail with  update option 
    path('exam-detail/',views.examDetailView.as_view(),name='exam_detail'),
    path('request-registration/<examId>/',views.requestRegistrationView.as_view(),name='request_registration'),
    path('accept-registration/',views.acceptRegistrationView.as_view(),name='accept_registration'),
    path('set-questions/',views.setQuestionView.as_view(),name='set_questions'),
    path('exam-questions/',views.questionsView.as_view(),name='questionsView'),
    ##question detail with update option
    path('question-detail/',views.questionDetailView.as_view(),name='questionDetailView'),
    path('registered-exams/',views.registeredExamView.as_view(),name='registered_exam'),
    path('get-question/',views.getQuestionView.as_view(),name='get_question'),
    path('submit-answer/',views.submitAnswersView.as_view(),name='submit_answer'),
    ]