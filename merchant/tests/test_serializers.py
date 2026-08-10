from django.test import TestCase
from django.contrib.auth.models import User

from merchant import models
from merchant import serializers


class MerchantSerializerCreateTest(TestCase):

    def setUp(self):
        self.status = models.StatusMerchant.objects.create(
            status_name="draft"
        )

        self.valid_data = {
            "cnpj": "12345678000199",
            "razao_social": "Empresa Teste LTDA",
            "nome_fantasia": "Empresa Teste",
            "email": "teste@empresa.com",
            "telefone": "67999999999",
            "status_id": self.status.id,
        }

    def test_deve_aceitar_dados_validos(self):
        serializer = serializers.MerchantSerializerCreate(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_rejeitar_campo_nao_permitido(self):
        data = self.valid_data.copy()
        data["campo_invalido"] = "teste"

        serializer = serializers.MerchantSerializerCreate(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "detail",
            serializer.errors
        )

        self.assertIn(
            "campo_invalido",
            str(serializer.errors["detail"])
        )

    def test_deve_aceitar_nome_fantasia_nulo(self):
        data = self.valid_data.copy()
        data["nome_fantasia"] = ''

        serializer = serializers.MerchantSerializerCreate(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_status_id_deve_ser_convertido_para_status(self):
        serializer = serializers.MerchantSerializerCreate(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["status"],
            self.status
        )

    def test_status_inexistente_deve_ser_rejeitado(self):
        data = self.valid_data.copy()
        data["status_id"] = 999999

        serializer = serializers.MerchantSerializerCreate(
            data=data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "status_id",
            serializer.errors
        )


class MerchantSerializerUpdateTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "cnpj": "12345678000199",
            "razao_social": "Empresa Teste LTDA",
            "nome_fantasia": "Empresa Teste",
            "email": "teste@empresa.com",
            "telefone": "67999999999",
        }

    def test_deve_aceitar_dados_validos(self):
        serializer = serializers.MerchantSerializerUpdate(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_rejeitar_status(self):
        data = self.valid_data.copy()
        data["status"] = 1

        serializer = serializers.MerchantSerializerUpdate(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "detail",
            serializer.errors
        )

        self.assertIn(
            "status",
            str(serializer.errors["detail"])
        )

    def test_deve_rejeitar_campo_nao_permitido(self):
        data = self.valid_data.copy()
        data["id"] = 10

        serializer = serializers.MerchantSerializerUpdate(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "detail",
            serializer.errors
        )


class MerchantSerializerTest(TestCase):

    def setUp(self):
        self.status = models.StatusMerchant.objects.create(
            status_name="approved"
        )

        self.merchant = models.Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.status,
        )

    def test_deve_retornar_status_name(self):
        serializer = serializers.MerchantSerializer(
            self.merchant
        )

        data = serializer.data

        self.assertEqual(
            data["status_name"],
            "approved"
        )

    def test_deve_retornar_status_id(self):
        serializer = serializers.MerchantSerializer(
            self.merchant
        )

        data = serializer.data

        self.assertEqual(
            data["status_id"],
            self.status.id
        )

    def test_deve_retornar_dados_do_merchant(self):
        serializer = serializers.MerchantSerializer(
            self.merchant
        )

        data = serializer.data

        self.assertEqual(
            data["cnpj"],
            "12345678000199"
        )

        self.assertEqual(
            data["razao_social"],
            "Empresa Teste LTDA"
        )


class MerchantUpdateStatusSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_teste",
            password="123456"
        )

        self.status = models.StatusMerchant.objects.create(
            status_name="pending_analysis"
        )

        self.valid_data = {
            "user_id": self.user.id,
            "status": self.status.id,
            "motivo": "Documentação analisada",
        }

    def test_deve_aceitar_dados_validos(self):
        serializer = serializers.MerchantUpdateStatusSerializer(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_aceitar_motivo_ausente(self):
        data = self.valid_data.copy()
        del data["motivo"]

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_aceitar_motivo_nulo(self):
        data = self.valid_data.copy()
        data["motivo"] = None

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_aceitar_motivo_vazio(self):
        data = self.valid_data.copy()
        data["motivo"] = ""

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_deve_rejeitar_campo_nao_permitido(self):
        data = self.valid_data.copy()
        data["status_id"] = self.status.id

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "detail",
            serializer.errors
        )

    def test_user_id_deve_ser_convertido_para_user(self):
        serializer = serializers.MerchantUpdateStatusSerializer(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["user_id"],
            self.user
        )

    def test_status_deve_ser_convertido_para_status(self):
        serializer = serializers.MerchantUpdateStatusSerializer(
            data=self.valid_data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["status"],
            self.status
        )

    def test_user_inexistente_deve_ser_rejeitado(self):
        data = self.valid_data.copy()
        data["user_id"] = 999999

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "user_id",
            serializer.errors
        )

    def test_status_inexistente_deve_ser_rejeitado(self):
        data = self.valid_data.copy()
        data["status"] = 999999

        serializer = serializers.MerchantUpdateStatusSerializer(
            data=data
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "status",
            serializer.errors
        )


class StatusMerchantSerializerTest(TestCase):

    def setUp(self):
        self.status = models.StatusMerchant.objects.create(
            status_name="draft"
        )

    def test_deve_serializar_status(self):
        serializer = serializers.StatusMerchantSerializer(
            self.status
        )

        self.assertEqual(
            serializer.data["id"],
            self.status.id
        )

        self.assertEqual(
            serializer.data["status_name"],
            "draft"
        )


class MerchantStatusHistorySerializerTest(TestCase):

    def setUp(self):
        self.status = models.StatusMerchant.objects.create(
            status_name="draft"
        )

        self.user = User.objects.create_user(
            username="usuario_teste",
            password="123456"
        )

        self.merchant = models.Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.status,
        )

        self.historico = models.MerchantStatusHistory.objects.create(
            id_merchant=self.merchant,
            id_usuario=self.user,
            status_anterior=self.status,
            motivo="Teste",
        )

    def test_deve_serializar_historico(self):
        serializer = serializers.MerchantStatusHistorySerializer(
            self.historico
        )

        self.assertEqual(
            serializer.data["id"],
            self.historico.id
        )

        self.assertEqual(
            serializer.data["id_merchant"],
            self.merchant.id
        )

        self.assertEqual(
            serializer.data["id_usuario"],
            self.user.id
        )

        self.assertEqual(
            serializer.data["status_anterior"],
            self.status.id
        )

        self.assertEqual(
            serializer.data["motivo"],
            "Teste"
        )


class MerchantTimeLineViewTest(TestCase):

    def setUp(self):
        self.status = models.StatusMerchant.objects.create(
            status_name="draft"
        )

        self.user = User.objects.create_user(
            username="usuario_teste",
            password="123456"
        )

        self.merchant = models.Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.status,
        )

        self.historico = models.MerchantStatusHistory.objects.create(
            id_merchant=self.merchant,
            id_usuario=self.user,
            status_anterior=self.status,
            motivo="Merchant criado",
        )

    def test_deve_retornar_status_name(self):
        serializer = serializers.MerchantTimeLineView(
            self.historico
        )

        self.assertEqual(
            serializer.data["status_name"],
            "draft"
        )

    def test_deve_retornar_razao_social(self):
        serializer = serializers.MerchantTimeLineView(
            self.historico
        )

        self.assertEqual(
            serializer.data["razao_social"],
            "Empresa Teste LTDA"
        )

    def test_deve_retornar_motivo(self):
        serializer = serializers.MerchantTimeLineView(
            self.historico
        )

        self.assertEqual(
            serializer.data["motivo"],
            "Merchant criado"
        )


class LoginSerializerTest(TestCase):

    def test_deve_aceitar_username_e_password(self):
        data = {
            "username": "pedro",
            "password": "123456",
        }

        serializer = serializers.LoginSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_password_deve_ser_write_only(self):
        serializer = serializers.LoginSerializer()

        self.assertTrue(
            serializer.fields["password"].write_only
        )

    def test_username_e_obrigatorio(self):
        serializer = serializers.LoginSerializer(
            data={
                "password": "123456"
            }
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "username",
            serializer.errors
        )

    def test_password_e_obrigatorio(self):
        serializer = serializers.LoginSerializer(
            data={
                "username": "pedro"
            }
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "password",
            serializer.errors
        )