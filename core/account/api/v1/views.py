from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerialier,
    ProfileSerializer,
    ActivationResendSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404
from ..utils import EmailThread
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from ..utils import Util

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerialier

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = "bigdeli.ali3@gmail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/hello.tpl",
            {"token": token},
            "admin@admin.com",
            to=[self.email],
        )
        EmailThread(email_obj).start()
        return Response("email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response({"details": "your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account have been verified and activated successfully"}
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        data = {"request": request, "data": request.data}
        serializer = self.serializer_class(data=data)
        email = request.data["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = (
                "/accounts/api/v1/password-reset/" + uidb64 + "/" + token + "/"
            )
            absurl = "http://" + current_site + relativeLink
            email_body = (
                "Hive Group: Hello, Use this link  to reset password: " + absurl
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }
            Util.send_email(data)
        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {
                    "success": True,
                    "message": "Credentials Valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )
