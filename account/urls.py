from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/my_deck/', views.my_deck, name='my_deck'),
    path('signup/', views.UserSignUp.as_view(), name="signup"),
]
