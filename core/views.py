from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from .mongo import users_collection
from .auth_utils import generate_tokens, verify_token
import bcrypt  # type: ignore


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("userName")
        email = data.get("userEmail")
        password = data.get("userPassword")

        if not all([username, email, password]):
            return Response({"error": "Missing required fields"}, status=400)

        if users_collection.find_one({"email": email}):
            return Response({"message": "This email is already in use."}, status=400)

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        created_at = datetime.utcnow()
        user_doc = {
            "username": username,
            "email": email,
            "password": hashed_pw.decode(),
            "finalScore": None,
            "created_at": created_at,
            "updated_at": None,
            "credits": 0,
            "payments": [],
            "plan": "trial",
            "plan_expiration": None,
        }
        result = users_collection.insert_one(user_doc)
        access_token, refresh_token = generate_tokens(result.inserted_id)
        users_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"access_token": access_token, "refresh_token": refresh_token}},
        )
        return Response(
            {
                "userId": str(result.inserted_id),
                "username": username,
                "email": email,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "plan": "trial",
                "plan_expiration": None,
                "credits": 0,
                "payments": [],
                "created_at": created_at,
                "updated_at": None,
                "message": "User registered successfully.",
                "status": 201,
            }
        )


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
                "message": "Login successful",
            }
        )


class FinalScoreView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)
        if not user_id:
            return Response({"error": "Invalid or expired token"}, status=401)

        score = request.data.get("finalScore")
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"error": "User not found"}, status=404)

        if score is not None and (
            user.get("finalScore") is None or score > user["finalScore"]
        ):
            timestamp = datetime.utcnow()
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"finalScore": score, "saved_at": timestamp}},
            )
            return Response(
                {
                    "message": "Final score saved successfully.",
                    "saved_at": timestamp,
                },
                status=201,
            )

        return Response({"message": "New score not higher."}, status=200)


class LeaderboardView(APIView):
    def get(self, request):
        users = users_collection.find(
            {"finalScore": {"$ne": None}}, {"username": 1, "finalScore": 1, "_id": 0}
        ).sort("finalScore", -1)

        return Response(list(users))


class UserDetailView(APIView):
    def get(self, request, email):
        user = users_collection.find_one({"email": email})
        if not user:
            return Response({"message": "User not found"}, status=404)

        data = {
            "userId": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "finalScore": user.get("finalScore"),
        }
        return Response(data)
