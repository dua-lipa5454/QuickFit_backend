from .models import CustomUser, Avatar
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'user_image', 'clothing_image']
        extra_kwargs = {'password': {'write_only': True}, 'user_image': {'required': False}, 'clothing_image': {'required': False}}

    def create(self, validated_data):
        if CustomUser.objects.filter(phone_number=validated_data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Phone number is already in use."})

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )
        return user

    def update(self, instance, validated_data):
        # Update only fields that are provided
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        if 'user_image' in validated_data:
            instance.user_image = validated_data['user_image']
        if 'clothing_image' in validated_data:
            instance.clothing_image = validated_data['clothing_image']

        # Handle password update correctly
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the new password before saving

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  # Added write_only for security

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        return user
    

class AvatarSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ['id', 'name', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)
