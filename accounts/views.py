from django.contrib.auth import get_user_model

UserModel = get_user_model()

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg2.utils import swagger_auto_schema
from requests_html import HTMLSession

session = HTMLSession()

from root.settings import DEFAULT_EMAIL, MAILGUN_API_KEY
from .serializers import RegistrationSerializer
from .tokens import account_activation_token


RESPONSES = {
    200: "HTTP request successful",
    400: "Malformed request syntax",
    500: "An internal server error occured",
}


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        operation_description="Register users",
        operation_summary="Registration View",
        responses={
            201: "Object creation successful",
            400: "Malformed request syntax",
            500: "An internal server error occured",
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_id = serializer.data["id"]
            message = "User created successfully"
            token = Token.objects.get(user=user)
            current_site = get_current_site(request).domain
            subject = "Dancrest: Activate Your Account"
            html_message = render_to_string(
                "emails/account_activation.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user_id)),
                    "token": account_activation_token.make_token(user),
                },
            )

            session.post(
                "https://api.mailgun.net/v3/sandbox5301a79097994dd5a621705473034cc2.mailgun.org/messages",
                auth=("api", MAILGUN_API_KEY),
                data={
                    "from": DEFAULT_EMAIL,
                    "to": [user.email],
                    "subject": subject,
                    "text": html_message,
                },
            )

            response = {
                "status": "success",
                "message": message,
                "data": {
                    "id": user_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_no,
                    "is_verified": user.is_verified,
                    "date_joined": user.date_joined,
                    "token": token.key,
                },
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {
                "status": "error",
                "message": "Invalid request",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class AccountActivationView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Activate email of users",
        operation_summary="Account Activation View",
        responses=RESPONSES,
        tags=["Authentication"],
    )
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user is not None and account_activation_token.check_token(
            user, token
        ):
            user.is_verified = True
            user.save()
            return render(request, "emails/account_activation_success.html")
        return HttpResponse("Invalid activation link!!")
