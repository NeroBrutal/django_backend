from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from bson.objectid import ObjectId
from ..mongo import users_collection
from ..auth_utils import verify_token


class FinalScoreView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        print(f"Token: {token}")
        user_id = verify_token(token)
        if not user_id:
            return Response({"error": "Invalid or expired token"}, status=401)

        score = int(request.data.get("finalScore"))
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
                    "userId": str(user["_id"]),
                    "username": user["username"],
                    "email": user["email"],
                    "finalScore": score,
                    "created_at": user["created_at"],
                    "updated_at": user["updated_at"],
                    "plan": user["plan"],
                    "credits": user["credits"],
                    "payments": user["payments"],
                },
                status=201,
            )

        return Response({"message": "New score not higher."}, status=200)
