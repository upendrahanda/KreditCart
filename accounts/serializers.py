from rest_framework import serializers

from .models import CustomUser


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', )
