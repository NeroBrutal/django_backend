from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from ..mongo import users_collection
from ..auth_utils import generate_tokens
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
                "credits": 0,
                "payments": [],
                "created_at": created_at,
                "updated_at": None,
                "message": "User registered successfully.",
                "status": 201,
            }
        )
