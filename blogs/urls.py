from django.urls import path
from blogs.views import (
    BlogListView, BlogCreateView, 
    BlogDetailView, BlogUpdateView, BlogDeleteView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]