from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateRideSerializer, RideSerializer
from users.permissions import IsRider


class CreateRideView(APIView):
    permission_classes = [IsRider]

    def post(self, request):
        serializer = CreateRideSerializer(data=request.data)
        if serializer.is_valid():
            ride =serializer.save(rider=request.user)
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)