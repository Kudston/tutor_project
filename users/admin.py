from django.contrib import admin
from .models import   (userProfile,
                        Tutor,Exam,Question,
                        answeredQuestion,examSheet,
                        examRegistrationLink,
                        examRequestObject,
                        examRecordSheet)

# Register your models here.
admin.site.register(userProfile)
admin.site.register(Tutor)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(answeredQuestion)
admin.site.register(examSheet)
admin.site.register(examRequestObject)
admin.site.register(examRegistrationLink)
admin.site.register(examRecordSheet)