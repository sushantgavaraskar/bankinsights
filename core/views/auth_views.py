from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.user_serializer import UserRegisterSerializer, UserLoginSerializer
import logging
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import User  # Add this import for the User model

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
        logger.info(f"Registration attempt: {request.data.get('email')}")
        email = request.data.get("email")
        full_name = request.data.get("full_name")
        password = request.data.get("password")

        if not email or "@" not in email:
            return Response({"detail": "Invalid email."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=400)

        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "email": user.email,
                "full_name": user.full_name
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
    
})

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logger.info(f"Login attempt: {request.data.get('email')}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            logger.info(f"User logged in: {user.email}")
            return Response({"tokens": tokens, "email": user.email, "is_superuser": user.is_superuser,}, status=status.HTTP_200_OK)
        logger.warning(f"Login failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "full_name": user.full_name
        })

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Password change attempt for user: {request.user.email}")
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password changed successfully."})