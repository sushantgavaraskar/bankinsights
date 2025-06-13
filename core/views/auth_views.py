from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.user_serializer import UserRegisterSerializer, UserLoginSerializer
import logging
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            logger.info(f"User registered: {user.email}")
            return Response({"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            logger.info(f"User logged in: {user.email}")
            return Response({"tokens": tokens, "email": user.email, "is_superuser": user.is_superuser,}, status=status.HTTP_200_OK)
        logger.warning(f"Login failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
