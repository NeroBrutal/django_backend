from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from bson.objectid import ObjectId
from ..mongo import users_collection
from ..auth_utils import verify_token
from dateutil.relativedelta import relativedelta


class UpdatePlanView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        print("user", user)
        if not user:
            return Response({"error": "Invalid or expired token"}, status=401)

        data = request.data
        plan = data.get("plan")
        user_plan = user.get("plan")
        if user_plan == plan:
            return Response(
                {"error": "You are already subscribed to this plan."}, status=400
            )
        if plan == "basic":
            credits = 500
        elif plan == "premium":
            credits = 1000
        elif plan == "pro":
            credits = 2000
        expiration_date = datetime.now(timezone.utc) + relativedelta(months=1)
        card_number = data.get("cardNumber")
        if not plan or not card_number:
            return Response({"error": "Missing required fields"}, status=400)
        timestamp = datetime.now(timezone.utc)
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "plan": plan,
                    "updated_at": timestamp,
                    "credits": int(user["credits"] + credits),
                    "payments": [
                        {
                            "plan": plan,
                            "expiration_date": expiration_date,
                            "card_number": card_number,
                            "created_at": timestamp,
                        }
                    ],
                }
            },
        )

        return Response(
            {
                "message": "Plan updated successfully.",
                "userId": str(user_id),
                "plan": plan,
                "updated_at": datetime.utcnow(),
                "credits": int(user["credits"] + credits),
                "payments": [
                    {
                        "plan": plan,
                        "expiration_date": expiration_date,
                        "card_number": card_number,
                        "created_at": timestamp,
                    }
                ],
                "created_at": user.get("created_at"),
                "finalScore": user.get("finalScore"),
                "username": user.get("username"),
                "email": user.get("email"),
            },
            status=200,
        )
