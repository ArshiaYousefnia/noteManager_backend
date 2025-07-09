from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()
USERNAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$'

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['email'].required = True
        else:
            self.fields['email'].required = False

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate_username_format(self, value):
        if not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError(
                "Username must start with a letter and contain only letters, digits, or underscores. "
                "Length must be between 3 and 30 characters."
            )
        return value
