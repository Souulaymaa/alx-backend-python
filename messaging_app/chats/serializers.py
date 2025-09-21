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
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

    def validate(self, data):
        if data['first_name'].lower() == data['last_name'].lower():
            raise serializers.ValidationError("First name and last name cannot be identical")
        return data

# ------------------------
# Message Serializer
# ------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value

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
