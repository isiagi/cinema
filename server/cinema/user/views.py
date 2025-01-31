from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings
from user.models import User

# 🔹 User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# 🔹 Profile View - Includes Active Status
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_active": user.is_active  # ✅ Check if user is active
        })

# 🔹 Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# 🔹 Login View - Ensures Only Active Users Can Log In
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate user and return JWT tokens if active.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_active:
                return Response({"message": "Your account is inactive."}, status=403)

            refresh_token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
            })
        return Response({"message": "Invalid credentials"}, status=400)

# 🔹 Logout View - Invalidates Token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate refresh token (blacklist it).
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"message": "Refresh token is required."}, status=400)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception:
            return Response({"message": "Invalid or expired token."}, status=400)

# 🔹 Account Creation
class CreateAccountView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": UserSerializer(user).data
            }, status=201)
        return Response(serializer.errors, status=400)

# 🔹 Update Profile
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Fully update the user's profile.
        """
        user = request.user
        user.name = request.data.get("name", user.name)
        user.save()
        return Response({"message": "Profile updated successfully"}, status=200)

    def patch(self, request):
        """
        Partially update the user's profile.
        """
        user = request.user
        for key, value in request.data.items():
            setattr(user, key, value)
        user.save()
        return Response({"message": "Profile updated successfully"}, status=200)

# 🔹 Forgot Password
class ForgotPasswordView(APIView):
    def post(self, request):
        """
        Send password reset link to user's email.
        """
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)

        # Generate password reset token and send email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{request.build_absolute_uri('/reset-password/')}{uid}/{token}/"

        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({"message": "Password reset link sent successfully"}, status=200)

# 🔹 Reset Password
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        """
        Reset user's password using the provided token.
        """
        new_password = request.data.get("new_password")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"}, status=200)
            else:
                return Response({"message": "Invalid token"}, status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid user"}, status=400)

# 🔹 Verify Email
class VerifyEmailView(APIView):
    def post(self, request):
        """
        Verify user email using token.
        """
        token = request.data.get("token")

        try:
            refresh_token = RefreshToken(token)
            user_id = refresh_token.payload.get("user_id")
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=200)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=404)
        except Exception as e:
            return Response({"message": str(e)}, status=400)
