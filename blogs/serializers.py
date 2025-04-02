from rest_framework import serializers
from blogs.models import Blog


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

