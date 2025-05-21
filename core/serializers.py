from rest_framework import serializers
from .models import User
from bson import ObjectId


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId")


class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'finalScore']
        extra_kwargs = {
            'password': {'write_only': True}
        }
