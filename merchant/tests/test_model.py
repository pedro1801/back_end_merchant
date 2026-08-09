from django.test import TestCase
from django.contrib.auth.models import User

from merchant.models import StatusMerchant, Merchant, MerchantStatusHistory

class StatusMerchantModelTestCase(TestCase):

    def test_criar_status_merchant(self):
        status = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.assertIsNotNone(status.id)
        self.assertEqual(status.status_name, "draft")

class MerchantModelTestCase(TestCase):

    def test_criar_merchant(self):
        status = StatusMerchant.objects.create(
            status_name="draft"
        )

        merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            email="empresa@email.com",
            telefone="67999999999",
            status=status,
        )

        self.assertIsNotNone(merchant.id)
        self.assertEqual(merchant.cnpj, "12345678000199")
        self.assertEqual(
            merchant.razao_social,
            "Empresa Teste LTDA"
        )
        self.assertEqual(
            merchant.nome_fantasia,
            "Empresa Teste"
        )
        self.assertEqual(
            merchant.status,
            status
        )

class MerchantStatusHistoryModelTestCase(TestCase):

    def test_criar_historico_status(self):
        status_anterior = StatusMerchant.objects.create(
            status_name="draft"
        )

        status_atual = StatusMerchant.objects.create(
            status_name="pending_analysis"
        )

        usuario = User.objects.create_user(
            username="usuario_teste",
            email="usuario@teste.com",
            password="123456"
        )

        merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            email="empresa@email.com",
            telefone="67999999999",
            status=status_atual,
        )

        historico = MerchantStatusHistory.objects.create(
            id_merchant=merchant,
            id_usuario=usuario,
            status_anterior=status_anterior,
            motivo="Draft para Pending Analysis",
        )

        self.assertIsNotNone(historico.id)

        self.assertEqual(
            historico.id_merchant,
            merchant
        )

        self.assertEqual(
            historico.id_usuario,
            usuario
        )

        self.assertEqual(
            historico.status_anterior,
            status_anterior
        )


        self.assertEqual(
            historico.motivo,
            "Draft para Pending Analysis"
        )