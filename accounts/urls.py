from distutils.log import Log
from django.urls import path
from .views import SignUpView, LoginView, LogoutView
from . import views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/<int:pk>/', views.profile, name='user-profile'),
    path('profile/update/', views.profileUpdate, name='profile-update'),
    path('profile/stars/<int:pk>/', views.startView, name='user_stars'),
]


