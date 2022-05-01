from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta: 
        model = User
        exclude = ['password']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        print(validated_data)
        # Save user details
        user = instance.user
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data.get('password'))
        user.save()
        # Save profile details
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def create(self, validated_data):
        user = User.objects.create(**validated_data.pop('user', {}))
        profile = Profile.objects.create(**validated_data)
        profile.user = user
        return profile
        