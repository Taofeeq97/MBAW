from django.shortcuts import render
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer

from blogs.models import Blog, Subscriber, JobApplication
from blogs.pagination import CustomPagination
from blogs.serializers import BlogSerializer, SubscriberSerializer, UserSerializer, JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 
    

class BlogCreateView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        blog = serializer.save(created_by=self.request.user)
        subscribers = Subscriber.objects.all()
        
        context = {
            'blog_title': blog.title,
            'blog_excerpt': blog.content[:200] + '...' if len(blog.content) > 200 else blog.content,
            'blog_image': blog.image.url if blog.image else None,
            'blog_url': f"",
            'unsubscribe_url': f"",
            'website_url': '',
            'current_year': "",
        }
        
        html_content = render_to_string('email_template.html', context)
        
        msg = EmailMultiAlternatives(
            subject=f"New Blog Post: {blog.title}",
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email for sub in subscribers],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class BlogListView(ListAPIView):
    queryset = Blog.objects.all()[:6]
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    

class BlogUpdateView(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)


class BlogDeleteView(DestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            instance.delete()
            return Response(
                {"success": "Blog post deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog post not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class SubscriberCreateView(CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class SubscriberDetailView(RetrieveAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]


class SubscriberListView(ListAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


class SubscriberUpdateView(UpdateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class SubscriberDeleteView(DestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()


class ContactUsView(APIView):
    permission_classes = [] 

    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            context = serializer.validated_data
            context['site_name'] = "Made by Akin"
            
            html_content = render_to_string('contact_us_email.html', context)
            
            email = EmailMultiAlternatives(
                subject=f"New Contact Form Submission: {context['subject']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['otutaofeeqi@gmail.com', 'olatubosunoluwaseyi1@gmail.com'],
                reply_to=[context['email']]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return Response({"message": "Thank you for contacting us!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class JobApplicationView(APIView):
    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the job application
            job_application = serializer.save()
            
            # Prepare context for email template
            context = {
                'job_title': job_application.job_title,
                'full_name': job_application.full_name,
                'email': job_application.email,
                'phone_number': job_application.phone_number,
                'cover_letter': job_application.cover_letter,
                'resume_url': request.build_absolute_uri(job_application.resume.url),
                'subject': f"Job Application for {job_application.job_title}"
            }
            
            html_content = render_to_string('job_application.html', context)
            email = EmailMultiAlternatives(
                subject=f"New Job Application: {job_application.job_title}",
                body=f"New job application received from {job_application.full_name}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['otutaofeeqi@gmail.com', 'olatubosunoluwaseyi1@gmail.com'],
                reply_to=[job_application.email]
            )
            email.attach_alternative(html_content, "text/html")
            try:
                email.send()
                return Response({
                    'message': 'Your job application has been submitted successfully!',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'message': 'Your job application has been submitted, but there was an issue sending the notification email.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            