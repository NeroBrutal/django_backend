from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if not all(
            [data.get("userName"), data.get("userEmail"), data.get("userPassword")]
        ):
            return Response({"error": "Missing required fields"}, status=400)

        if User.objects.filter(email=data["userEmail"]).exists():
            return Response({"message": "This email is already in use."}, status=400)

        if User.objects.filter(username=data["userName"]).exists():
            return Response({"message": "This username is already taken."}, status=400)

        user = User(
            username=data["userName"],
            email=data["userEmail"],
            password=data["userPassword"],
            finalScore=None,
        )
        user.save()
        serializer = UserSerializer(user)
        return Response(
            {
                **serializer.data,
                "message": "User registered successfully.",
                "status": 201,
            }
        )


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(email=data.get("userEmail")).first()
        if not user:
            return Response({"error": "User not found."}, status=404)

        if user.password != data.get("userPassword"):
            return Response({"error": "Invalid credentials."}, status=401)

        return Response(
            {
                "userId": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Login successful",
            }
        )


class FinalScoreView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(email=data.get("userEmail")).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        score = data.get("finalScore")
        if score is not None and (user.finalScore is None or score > user.finalScore):
            user.finalScore = score
            user.save()
            return Response({"message": "Final score saved successfully."}, status=201)

        return Response({"message": "New score not higher."}, status=200)


class LeaderboardView(APIView):
    def get(self, request):
        users = (
            User.objects.all().order_by("-finalScore").values("username", "finalScore")
        )
        return Response(users)


class UserDetailView(APIView):
    def get(self, request, email):
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "User not found"}, status=404)

        data = UserSerializer(user).data
        return Response(data)
