from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class MerchantSerializerCreate(serializers.ModelSerializer):
    status_id = serializers.PrimaryKeyRelatedField(
        source="status",
        queryset=models.StatusMerchant.objects.all()
    )

    def validate(self, attrs):
        allowed_fields = {
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "email",
            "telefone",
            "status_id",
        }

        receved_fields = set(self.initial_data.keys())

        extra_fields = receved_fields - allowed_fields

        if extra_fields:
            raise serializers.ValidationError({
                "detail": (
                    f"Campos não permitidos: "
                    f"{', '.join(extra_fields)}"
                )
            })

        return attrs

    class Meta:
        model = models.Merchant
        fields = [
            "id",
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "email",
            "telefone",
            "data_criacao",
            "status_id",
        ]

class MerchantSerializerUpdate(serializers.ModelSerializer):

    def validate(self, attrs):
        allowed_fields = {
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "email",
            "telefone",
        }

        receved_fields = set(self.initial_data.keys())

        extra_fields = receved_fields - allowed_fields

        if extra_fields:
            raise serializers.ValidationError({
                "detail": (
                    f"Campos não permitidos: "
                    f"{', '.join(extra_fields)}"
                )
            })

        return attrs
    
    class Meta:
        model = models.Merchant
        fields = [
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "email",
            "telefone",
        ]

class MerchantSerializer(serializers.ModelSerializer):
    status_id = serializers.PrimaryKeyRelatedField(
        source="status",
        queryset=models.StatusMerchant.objects.all()
    )

    status_name = serializers.CharField(
        source="status.status_name",
        read_only=True
    )

    class Meta:
        model = models.Merchant
        fields = [
            "id",
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "email",
            "telefone",
            "data_criacao",
            "status_id",
            "status_name",
        ]


class MerchantUpdateStatusSerializer(serializers.Serializer):

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    status = serializers.PrimaryKeyRelatedField(
        queryset=models.StatusMerchant.objects.all()
    )

    motivo = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    def validate(self, attrs):
        allowed_fields = {
            "user_id",
            "status",
            "motivo"
        }

        received_fields = set(self.initial_data.keys())

        extra_fields = received_fields - allowed_fields

        if extra_fields:
            raise serializers.ValidationError({
                "detail": (
                    f"Campos não permitidos: "
                    f"{', '.join(extra_fields)}"
                )
            })

        return attrs


class StatusMerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StatusMerchant
        fields = [
            "id",
            "status_name",
        ]


class MerchantStatusHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MerchantStatusHistory
        fields = [
            "id",
            "id_merchant",
            "id_usuario",
            "status_anterior",
            "motivo",
            "data_alteracao",
        ]

class MerchantTimeLineView(serializers.ModelSerializer):

    status_name = serializers.CharField(
        source="status_anterior.status_name",
        read_only=True
    )

    razao_social = serializers.CharField(
        source="id_merchant.razao_social",
        read_only=True
    )

    class Meta:
        model = models.MerchantStatusHistory
        fields = [
            "motivo",
            "status_name",
            "razao_social",
        ]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)