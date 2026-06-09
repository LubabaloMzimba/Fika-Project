from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, DriverProfileSerializer
from .permissions import IsDriver

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Account created successfully.',
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful.',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class DriverProfileView(APIView):
    permission_classes = [IsDriver]

    def get(self, request):
        try:
            profile = request.user.driver_profile
            serializer = DriverProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Driver profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    def post(self, request):
        try:
            request.user.driver_profile
            return Response(
                {'error': 'Driver profile already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            pass

        serializer = DriverProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)