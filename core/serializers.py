from rest_framework import serializers
from .models import User
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "finalScore"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_id(self, obj):
        return str(obj._id) if obj._id else None
