import json
from .serializers import ProfileSerializer
from rest_framework import viewsets
from .models import Profile
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
import datetime

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):

    model = Profile
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(methods=['post'], permission_classes=[AllowAny], detail=False)
    def signup(self, request):
        request_body = json.loads(request.body)
        print(request_body)
        standard = request_body.get('standard', None)
        roll_no = request_body.get('roll_no', None)
        section = request_body.get('section', None)
        year = datetime.datetime.now().year
        username = '{}{}{}{}'.format(year, standard, section, roll_no)
        try:
            new_user = User.objects.create(username=username)
            new_user.set_password(request_body.get('dob'))
            user_profile = new_user.profile
            for key, value in request_body.items():
                setattr(user_profile, key, value)
            new_user.save()
            user_profile.save()
            print(user_profile)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in e.args[0]:
                return Response({
                    'error': 'The user with the given details already exists. Please check the details and try again'
                })
            # print(e.args)
        return Response({'username': username})

    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=True)
    def change_password(self, request, pk=None):
        if pk:
            user = User.objects.get(username=pk)
            request_body = json.loads(request.body)
            old_password = request_body.get('old_password')
            new_password = request_body.get('new_password')

            if user.check_password(old_password) and self.validate_password(new_password):
                user.set_password(new_password)
                user.save()
                return Response(status=200, data={'message': 'Password changed successfully'})

    def validate_password(self, password):
        return isinstance(password, str) and len(password) >= 8
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def signin(self, request, pk=None):
        user = None
        if pk:
            try:
                user = User.objects.get(username=pk)
            except User.DoesNotExist:
                return Response({'error': 'Entered username does not exist'}, status=401)
            generated_token_object = Token.objects.get(user=user)
            generated_token_string = generated_token_object.key

            if request.auth.key == generated_token_string:
                user_profile = Profile.objects.get(user=user)
                if user_profile.auth_token == '0':
                    user_profile.auth_token = request.auth.key
                    user_profile.save()
                    return Response(status=200, data={'message': 'Login Successful', 'token': request.auth.key})
                else:
                    user_profile.auth_token = '0'
                    user_profile.save()
                    return Response(status=401, data={'error': 'Another session was alrready in progress. You have been logged out of that session. Please login again', 'token': '0'})

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def signout(self, request):
        token_object = Token.objects.get(key=request.auth.key)
        username = token_object.user.username
        print(username)
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)
        user_profile.auth_token = '0'
        user_profile.save()
        return Response(status=200, data={'message': 'Logout Successful'})
