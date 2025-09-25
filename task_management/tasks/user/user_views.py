from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .user_serializer import RegisterSerializer, LoginSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..models import User




class RegisterApi(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPi(APIView):
    def post(self,request):
        serialized=LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        return Response(serialized.validated_data,status=status.HTTP_200_OK)
    
class UserProfileApi(APIView):
    permission_classes = [IsAuthenticated]  

    def patch(self, request):
        user = request.user 
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        user = request.user
        user_data = User.objects.filter(username=user.username)

        serializer = UserProfileSerializer(user_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    