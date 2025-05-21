from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    FinalScoreView,
    LeaderboardView,
    UserDetailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("final-score/", FinalScoreView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),
    path("user/<str:email>/", UserDetailView.as_view()),
]
