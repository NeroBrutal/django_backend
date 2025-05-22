from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from ..mongo import users_collection
import bcrypt  # type: ignore


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
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
            "plan": user["plan"],
            "credits": user["credits"],
            "payments": user["payments"],
        }
        return Response(data)

    def put(self, request, email):
        user = users_collection.find_one({"email": email})
        if not user:
            return Response({"message": "User not found"}, status=404)

        data = request.data
        updated_data = {}
        if "userName" in data:
            updated_data["username"] = data["userName"]
        if "userPassword" in data:
            updated_data["password"] = bcrypt.hashpw(
                data["userPassword"].encode(), bcrypt.gensalt()
            ).decode()

        if updated_data:
            users_collection.update_one({"email": email}, {"$set": updated_data})

        return Response(
            {
                "message": "User details updated successfully.",
                "userId": str(user["_id"]),
                "username": updated_data.get("username", user["username"]),
                "email": updated_data.get("email", user["email"]),
                "finalScore": updated_data.get("finalScore", user["finalScore"]),
                "created_at": updated_data.get("created_at", user["created_at"]),
                "updated_at": updated_data.get("updated_at", user["updated_at"]),
                "plan": updated_data.get("plan", user["plan"]),
                "credits": updated_data.get("credits", user["credits"]),
                "payments": updated_data.get("payments", user["payments"]),
            },
            status=200,
        )

    def delete(self, request, email):
        user = users_collection.find_one({"email": email})
        if not user:
            return Response({"message": "User not found"}, status=404)

        users_collection.delete_one({"email": email})
        return Response({"message": "User deleted successfully."}, status=200)
