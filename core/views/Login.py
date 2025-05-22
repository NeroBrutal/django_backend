from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from ..mongo import users_collection
from ..auth_utils import generate_tokens
import bcrypt  # type: ignore


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("userEmail")
        password = data.get("userPassword")

        user = users_collection.find_one({"email": email})
        if not user:
            return Response({"error": "User not found."}, status=404)

        if not bcrypt.checkpw(password.encode(), user["password"].encode()):
            return Response({"error": "Invalid credentials."}, status=401)

        access_token, refresh_token = generate_tokens(user["_id"])
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"access_token": access_token, "refresh_token": refresh_token}},
        )

        return Response(
            {
                "userId": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "access_token": access_token,
                "refresh_token": refresh_token,
                "plan": user["plan"],
                "credits": user["credits"],
                "payments": user["payments"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
                "finalScore": user.get("finalScore"),
                "status": 200,
                "message": "Login successful",
            }
        )
