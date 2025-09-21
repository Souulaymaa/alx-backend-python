# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'password']

    def create(self, validated_data):
        # Use set_password to hash password
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

# ------------------------
# Message Serializer
# ------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at']

# ------------------------
# Conversation Serializer
# ------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_messages(self, obj):
        # Return serialized messages for this conversation
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
