from apps.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class ManagerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'password']

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu phone allaqachon mavjud")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            **validated_data,
            role='manager',
            is_staff=True
        )
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        user = authenticate(phone=phone, password=password)

        if not user:
            raise serializers.ValidationError("Phone yoki password noto‘g‘ri")

        if not user.is_active:
            raise serializers.ValidationError("User active emas")

        data['user'] = user
        return data
