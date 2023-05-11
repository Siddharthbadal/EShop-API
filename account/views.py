from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.utils.crypto import get_random_string
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.utils import timezone
from utilis.helpers import get_current_host

@api_view(['POST'])
def register(request):
    data = request.data 

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email = data['email'],
                username= data['email'],
                password = make_password(data['password'])
            )

            return Response({'details':'User Registered'}, status=status.HTTP_200_OK)


        else:
            return Response({'details': "User already exists!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    user = request.user
    data = request.data 
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email= data['email']

   

    user.save()
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_password(request):
     """
        update the user password
     """
     user = request.user
     data = request.data 

     if data['password'] != "":
        user.password = make_password(data['password'])

     user.save()
     serializer = UserSerializer(user, many=False)

     return Response(serializer.data)





@api_view(['POST'])
def forgot_password(request):
    """
        send a password reset link to registered user email to change password.
    """
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(40)
    expire_date=datetime.now() + timedelta(minutes=30)

    user.userprofile.reset_password_token=token
    user.userprofile.reset_password_expire=expire_date

    user.userprofile.save()
    host= get_current_host(request)
    print(host)

    link = "{host}api/reset_password/{token}".format(host=host, token=token)
    print(link)
    body = "Your password reset link is: {link}".format(link=link)
    subject="Password Reset link for EShop"
    send_mail(subject, 
              body, 
              "noreply@eshop.com",
              [data['email']]
            )
    return Response({'details':" Password reset email sent to {email}".format(email=data['email'])})



@api_view(['POST'])
def reset_password(request, token):
    """
    user recives an email to reset the password on registered email.
    user needs to enter password and confirmPassword.
    """
    data = request.data 
    user = get_object_or_404(User, userprofile__reset_password_token=token)
    # for time zone related issues 
    if user.userprofile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({'error': "Passwords doesn't match!"}, status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(data['password'])
    user.userprofile.reset_password_token= "" 

    user.userprofile.reset_password_expire = None 
    user.userprofile.save()
    user.save()
    return Response({"details": "Password reset done successfully!"})