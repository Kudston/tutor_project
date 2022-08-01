import jwt
import datetime 
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend


def accessTokenGenerator(id):
    return jwt.encode({
        'id':id,
        'iat':datetime.datetime.utcnow(),
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
    },"accessTokenGeneratorUser1243",algorithm="HS256")
    


def decodeAccessToken(token):
    return jwt.decode(token,"accessTokenGeneratorUser1243","HS256")

def refreshTokenGenerator(id):
    return jwt.encode({
        'id':id,
        'iat':datetime.datetime.utcnow(),
        'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    },"refreshTokenGeneratorUser1243",algorithm="HS256")

def decodeRefreshToken(token):
    return jwt.decode(token,"refreshTokenGeneratorUser1243","HS256")


# class authenticate_token(BaseBackend):
def isAuthenticated_user(request,token=None):
    auth = request.COOKIES['refreshToken']
    try:
        dec = decodeAccessToken(auth)
    except:
        dec = decodeRefreshToken(auth)
    userId = dec['id']
    user = User.objects.get(pk=userId)
    if request.user==user:
        return True
    else: return False
#     def get_user(self,user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
# def authenticated_user(request):
#     if request.user == authenticate_token.authenticate(request):
#         return True
#     else: return False 