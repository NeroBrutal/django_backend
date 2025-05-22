from django.urls import path

from core.views.Login import LoginView
from core.views.Register import RegisterView
from core.views.FinalScore import FinalScoreView
from core.views.UpdatePlan import UpdatePlanView
from core.views.UserDetail import UserDetailView
from core.views.Leaderboard import LeaderboardView
from core.views.RefreshToken import RefreshTokenView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("final-score/", FinalScoreView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),
    path("user/<str:email>/", UserDetailView.as_view()),
    path("updatePlan/", UpdatePlanView.as_view()),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
]
