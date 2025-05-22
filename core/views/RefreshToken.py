from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from bson.objectid import ObjectId
from ..mongo import users_collection
from ..auth_utils import generate_tokens, verify_token


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        user_id = verify_token(refresh_token)
        if not user_id:
            return Response({"error": "Invalid or expired refresh token"}, status=401)

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"error": "User not found"}, status=404)

        access_token, new_refresh_token = generate_tokens(user["_id"])
        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "access_token": access_token,
                    "refresh_token": new_refresh_token,
                }
            },
        )

        return Response(
            {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "userId": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "plan": user["plan"],
                "credits": user["credits"],
                "payments": user["payments"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
                "finalScore": user.get("finalScore"),
            },
            status=200,
        )
