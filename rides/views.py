import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateRideSerializer, RideSerializer
from users.permissions import IsRider, IsDriver
from .models import Ride



class CreateRideView(APIView):
    permission_classes = [IsRider]

    def post(self, request):
        serializer = CreateRideSerializer(data=request.data)
        if serializer.is_valid():
            ride =serializer.save(rider=request.user)
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AvailableRidesView(APIView):
    permission_classes = [IsDriver]

    def get(self, request):
        rides = Ride.objects.filter(status=Ride.REQUESTED, driver=None)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptRideView(APIView):
    permission_classes = [IsDriver]

    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        # availability check (the if statement above)
        if ride.status != Ride.REQUESTED or ride.driver is not None:
            return Response({"error": "Ride is no longer available"}, status=status.HTTP_400_BAD_REQUEST)

        # update ride.driver, ride.status, save
        ride.driver = request.user
        ride.status = Ride.ACCEPTED
        ride.pickup_otp = str(random.randint(1000, 9999))
        ride.dropoff_otp = str(random.randint(1000, 9999))
        ride.save()


        return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
    

class StartRideView(APIView):
    permission_classes = [IsDriver]

    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        if ride.driver != request.user:
            return Response({"error": "Ride does not belong to you"}, status=status.HTTP_403_FORBIDDEN)

        if ride.status != Ride.ACCEPTED:
            return Response({"error": "Ride cannot be started"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('pickup_otp') != ride.pickup_otp:
            return Response({"error": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = Ride.ONGOING
        ride.save()

        return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)