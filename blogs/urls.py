from django.urls import path
from blogs.views import (
    BlogListView, BlogCreateView, 
    BlogDetailView, BlogUpdateView, 
    BlogDeleteView, SubscriberListView,
    SubscriberCreateView, SubscriberUpdateView,
    SubscriberDeleteView, SubscriberDetailView, 
    UserCreateView, ContactUsView, JobApplicationView

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/register', UserCreateView.as_view(), name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('subscribers/', SubscriberListView.as_view(), name='subscriber-list'),
    path('subscribers/create/', SubscriberCreateView.as_view(), name='subscriber-create'),
    path('subscribers/<int:pk>/update/', SubscriberUpdateView.as_view(), name='subscriber-update'),
    path('subscribers/<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber-delete'),
    path('subscribers/<int:pk>/', SubscriberDetailView.as_view(), name='subscriber-detail'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('apply-job/', JobApplicationView.as_view(), name='apply_job'),
]