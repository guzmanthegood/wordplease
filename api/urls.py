from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('blogs/', views.BlogViewSet.as_view({'get': 'list'})),
    path('blogs/<str:username>/', views.PostList.as_view()),
]