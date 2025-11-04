from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile 

class RegisterSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'domain']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_username(self, value):
        """Проверяем, что имя пользователя уникально"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def create(self, validated_data):
        domain = validated_data.pop('domain', None)
        user = User.objects.create_user(**validated_data)
       

        # создаём первую задачу сканирования с введённым доменом
        UserProfile.objects.get_or_create(user=user,  defaults={"domain": domain})
        return user
