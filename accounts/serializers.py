from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format="hex", read_only=True, required=False)

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_no",
            "is_verified",
            "password",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = self.validated_data["email"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        phone_no = self.validated_data["phone_no"]
        is_verified = self.validated_data["is_verified"]
        password = self.validated_data["password"]

        user = UserModel.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone_no,
            is_verified=is_verified,
        )
        user.set_password(password)
        user.save()
        return user
