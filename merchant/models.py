from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class StatusMerchant(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)

    class Meta:
        db_table = "status_merchant"

class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    cnpj = models.CharField(
        max_length=14, 
        unique=True,
        validators=[
            RegexValidator(
            regex=r'^\d{14}$',
            message='O CNPJ deve conter exatamente 14 números.'
        )
    ])
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(
        max_length=255,
        blank=True
    )
    email = models.EmailField() 
    telefone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='O telefone deve conter apenas números.'
            )
        ]
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey(
        StatusMerchant,
        on_delete=models.PROTECT,
        db_column="status_id",
    )

    class Meta:
        db_table = "merchant"

class MerchantStatusHistory(models.Model):
    id = models.AutoField(primary_key=True)

    id_merchant = models.ForeignKey(
        Merchant,
        on_delete=models.PROTECT,
        db_column="id_merchant"
    )

    id_usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="id_usuario"
    )

    status_anterior = models.ForeignKey(
        StatusMerchant,
        on_delete=models.PROTECT,
        db_column="status_anterior",
        related_name="historicos_status_anterior",
    )

    motivo = models.TextField(null=True)

    data_alteracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "merchant_status_history"