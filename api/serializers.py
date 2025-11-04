from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'domain']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        domain = validated_data.pop('domain', None)
        user = User.objects.create_user(**validated_data)
        # автоматически создается профиль (если есть сигнал)
        if hasattr(user, 'profile'):
            user.profile.domain = domain
            user.profile.save()
        else:
            UserProfile.objects.create(user=user, domain=domain)
        return user
