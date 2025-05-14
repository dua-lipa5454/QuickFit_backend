from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, LoginSerializer, AvatarSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser, Avatar  # Ensure you're using CustomUser, not Django's default User
from django.views.decorators.http import require_GET

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    parser_classes = (MultiPartParser, FormParser)  # Handle file uploads

    def patch(self, request, *args, **kwargs):
        user = request.user  # Get the logged-in user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Image uploaded successfully', 'image_url': user.user_image.url}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UploadClothingImageView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can upload
    parser_classes = (MultiPartParser, FormParser)  # Handle file uploads

    def patch(self, request, *args, **kwargs):
        user = request.user  # Get the logged-in user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Clothing image uploaded successfully', 'image_url': user.clothing_image.url}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        try:
            user = request.user  # Get the authenticated user
            user_data = {
                'username': user.username,
                'email': user.email,
                'phone_number': user.profile.phone_number if hasattr(user, 'profile') else None  # If you have a profile model
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@require_GET
def avatar_list(request):
    avatars = Avatar.objects.all()
    data = [
        {"id": avatar.id,
         "name": avatar.name,
         "file_url": request.build_absolute_uri(avatar.file.url)}
        for avatar in avatars
    ]
    return JsonResponse({"avatars": data})