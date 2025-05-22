from rest_framework.views import APIView
from rest_framework.response import Response
from ..mongo import users_collection


class LeaderboardView(APIView):
    def get(self, request):
        users = users_collection.find(
            {"finalScore": {"$ne": None}}, {"username": 1, "finalScore": 1, "_id": 0}
        ).sort("finalScore", -1)

        return Response(list(users))
