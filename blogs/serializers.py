from django.contrib.auth.models import User
from rest_framework import serializers
from blogs.models import Blog, Subscriber, JobApplication
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class BlogSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'created_by',
            'uploaded_by',
            'image'
        ]

    def get_uploaded_by(self, obj):
        return obj.uploaded_by()


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id','email']

    def validate_email(self, value):
        if Subscriber.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class ContactUsSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100, required=True)
    email = serializers.CharField(required=True)
    phone_number = serializers.CharField(max_length=20, required=False)
    subject = serializers.CharField(max_length=200, required=True)
    message = serializers.CharField(required=True)

    def validate_email(self, value):
        try:
            validate_email(value)
            return value.lower()
        except ValidationError:
            raise serializers.ValidationError("Please enter a valid email address.")
        

class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=JobApplication
        fields = '__all__'

        