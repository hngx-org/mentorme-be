from rest_framework import serializers

from .models import Session, Category


class SessionSerializer(serializers.ModelSerializer):
    mentor = serializers.UUIDField(read_only=True)
    mentee = serializers.UUIDField(read_only=True)

    class Meta:
        model = Session
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
