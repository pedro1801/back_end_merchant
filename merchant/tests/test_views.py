from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from merchant.models import (
    Merchant,
    StatusMerchant,
    MerchantStatusHistory,
)


class MerchantCreateViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.url = reverse("merchant-create")

        self.valid_data = {
            "cnpj": "12345678000199",
            "razao_social": "Empresa Teste LTDA",
            "nome_fantasia": "Empresa Teste",
            "email": "teste@empresa.com",
            "telefone": "67999999999",
        }

    def test_get_deve_retornar_modelo_do_merchant(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("cnpj", response.data)
        self.assertIn("razao_social", response.data)
        self.assertIn("status_id", response.data)

    def test_post_deve_criar_merchant_com_status_draft(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Merchant.objects.count(),
            1
        )

        merchant = Merchant.objects.first()

        self.assertEqual(
            merchant.status,
            self.draft
        )

    def test_post_deve_retornar_dados_do_merchant(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["cnpj"],
            "12345678000199"
        )

        self.assertEqual(
            response.data["razao_social"],
            "Empresa Teste LTDA"
        )

    def test_post_nao_deve_aceitar_cnpj_duplicado(self):
        Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Existente",
            email="existente@empresa.com",
            telefone="67999999999",
            status=self.draft,
        )

        response = self.client.post(
            self.url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class MerchantListViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.url = reverse("merchant-list")

    def test_deve_listar_merchants(self):
        Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa 1",
            email="empresa1@teste.com",
            telefone="67999999999",
            status=self.draft,
        )

        Merchant.objects.create(
            cnpj="98765432000199",
            razao_social="Empresa 2",
            email="empresa2@teste.com",
            telefone="67988888888",
            status=self.draft,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )

    def test_sem_merchants_deve_retornar_404(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class MerchantIdViewTest(APITestCase):

    def setUp(self):
        self.status = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.status,
        )

    def test_deve_buscar_merchant_por_id(self):
        url = reverse(
            "merchant-id",
            kwargs={"merchant_id": self.merchant.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.merchant.id
        )

    def test_merchant_inexistente_deve_retornar_404(self):
        url = reverse(
            "merchant-id",
            kwargs={"merchant_id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class MerchantStatusViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.approved = StatusMerchant.objects.create(
            status_name="approved"
        )

        self.url = reverse(
            "merchant-status",
            kwargs={"status_id": self.draft.id}
        )

    def test_deve_listar_merchants_por_status(self):
        Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Draft",
            email="draft@teste.com",
            telefone="67999999999",
            status=self.draft,
        )

        Merchant.objects.create(
            cnpj="98765432000199",
            razao_social="Empresa Approved",
            email="approved@teste.com",
            telefone="67988888888",
            status=self.approved,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["status_name"],
            "draft"
        )

    def test_sem_merchant_para_status_deve_retornar_404(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class MerchantUpdateViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.approved = StatusMerchant.objects.create(
            status_name="approved"
        )

        self.merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Original",
            email="original@teste.com",
            telefone="67999999999",
            status=self.draft,
        )

        self.url = reverse(
            "merchant-update",
            kwargs={"merchant_id": self.merchant.id}
        )

    def test_deve_atualizar_merchant_em_draft(self):
        data = {
            "razao_social": "Empresa Alterada",
            "email": "alterado@teste.com",
        }

        response = self.client.put(
            self.url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.razao_social,
            "Empresa Alterada"
        )

        self.assertEqual(
            self.merchant.email,
            "alterado@teste.com"
        )

    def test_nao_deve_atualizar_merchant_fora_de_draft(self):
        self.merchant.status = self.approved
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "razao_social": "Tentativa de alteração"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.razao_social,
            "Empresa Original"
        )

    def test_merchant_inexistente_deve_retornar_404(self):
        url = reverse(
            "merchant-update",
            kwargs={"merchant_id": 999999}
        )

        response = self.client.put(
            url,
            {
                "razao_social": "Teste"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class MerchantUpdateStatusViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.pending = StatusMerchant.objects.create(
            status_name="pending_analysis"
        )

        self.approved = StatusMerchant.objects.create(
            status_name="approved"
        )

        self.rejected = StatusMerchant.objects.create(
            status_name="rejected"
        )

        self.blocked = StatusMerchant.objects.create(
            status_name="blocked"
        )

        self.user = User.objects.create_user(
            username="usuario_teste",
            password="123456"
        )

        self.merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.draft,
        )

        self.url = reverse(
            "merchant-update-status",
            kwargs={"merchant_id": self.merchant.id}
        )

    def test_get_deve_retornar_modelo(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("user_id", response.data)
        self.assertIn("status", response.data)
        self.assertIn("motivo", response.data)

    def test_draft_para_pending_analysis(self):
        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.pending.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.status,
            self.pending
        )

        historico = MerchantStatusHistory.objects.first()

        self.assertIsNotNone(historico)

        self.assertEqual(
            historico.status_anterior,
            self.draft
        )

        self.assertEqual(
            historico.motivo,
            "draft para pending_analysis"
        )

    def test_pending_analysis_para_approved(self):
        self.merchant.status = self.pending
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.approved.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.status,
            self.approved
        )

    def test_pending_analysis_para_rejected_exige_motivo(self):
        self.merchant.status = self.pending
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.rejected.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["detail"],
            "Motivo Obrigatorio"
        )

    def test_pending_analysis_para_rejected_com_motivo(self):
        self.merchant.status = self.pending
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.rejected.id,
                "motivo": "Documentação recusada",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.status,
            self.rejected
        )

        historico = MerchantStatusHistory.objects.first()

        self.assertEqual(
            historico.motivo,
            "Documentação recusada"
        )

    def test_approved_para_blocked_exige_motivo(self):
        self.merchant.status = self.approved
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.blocked.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["detail"],
            "Motivo Obrigatorio"
        )

    def test_approved_para_blocked_com_motivo(self):
        self.merchant.status = self.approved
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.blocked.id,
                "motivo": "Bloqueio solicitado",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.merchant.refresh_from_db()

        self.assertEqual(
            self.merchant.status,
            self.blocked
        )

    def test_transicao_nao_permitida(self):
        self.merchant.status = self.draft
        self.merchant.save()

        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.approved.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["detail"],
            "Status não permitido"
        )

    def test_status_inexistente(self):
        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": 999999,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["detail"],
            "Status não encontrado"
        )

    def test_merchant_inexistente(self):
        url = reverse(
            "merchant-update-status",
            kwargs={"merchant_id": 999999}
        )

        response = self.client.put(
            url,
            {
                "user_id": self.user.id,
                "status": self.pending.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_deve_criar_historico_ao_alterar_status(self):
        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.pending.id,
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            MerchantStatusHistory.objects.count(),
            1
        )

        historico = MerchantStatusHistory.objects.first()

        self.assertEqual(
            historico.id_merchant,
            self.merchant
        )

        self.assertEqual(
            historico.id_usuario,
            self.user
        )

        self.assertEqual(
            historico.status_anterior,
            self.draft
        )

    def test_deve_retornar_status_novo_na_resposta(self):
        response = self.client.put(
            self.url,
            {
                "user_id": self.user.id,
                "status": self.pending.id,
            },
            format="json"
        )
        
        self.assertEqual(
            response.data["status"],
            self.pending.id
        )


class MerchantTimeLineListViewTest(APITestCase):

    def setUp(self):
        self.draft = StatusMerchant.objects.create(
            status_name="draft"
        )

        self.user = User.objects.create_user(
            username="usuario_teste",
            password="123456"
        )

        self.merchant = Merchant.objects.create(
            cnpj="12345678000199",
            razao_social="Empresa Teste",
            email="teste@empresa.com",
            telefone="67999999999",
            status=self.draft,
        )

        self.url = reverse(
            "merchant-timeline",
            kwargs={"merchant_id": self.merchant.id}
        )

    def test_deve_retornar_timeline(self):
        MerchantStatusHistory.objects.create(
            id_merchant=self.merchant,
            id_usuario=self.user,
            status_anterior=self.draft,
            motivo="Merchant criado",
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["status_name"],
            "draft"
        )

        self.assertEqual(
            response.data[0]["razao_social"],
            "Empresa Teste"
        )

        self.assertEqual(
            response.data[0]["motivo"],
            "Merchant criado"
        )

    def test_merchant_inexistente_deve_retornar_404(self):
        url = reverse(
            "merchant-timeline",
            kwargs={"merchant_id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="pedro",
            password="123456",
            email="pedro@teste.com",
            first_name="Pedro",
            last_name="Teste",
        )

        self.url = reverse("login")

    def test_login_com_credenciais_validas(self):
        response = self.client.post(
            self.url,
            {
                "username": "pedro",
                "password": "123456",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["user_id"],
            self.user.id
        )

        self.assertEqual(
            response.data["username"],
            "pedro"
        )


    def test_login_com_senha_incorreta(self):
        response = self.client.post(
            self.url,
            {
                "username": "pedro",
                "password": "senha_errada",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.data["detail"],
            "Usuário ou senha inválidos"
        )

    def test_login_com_usuario_inexistente(self):
        response = self.client.post(
            self.url,
            {
                "username": "nao_existe",
                "password": "123456",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_login_sem_username(self):
        response = self.client.post(
            self.url,
            {
                "password": "123456",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_login_sem_password(self):
        response = self.client.post(
            self.url,
            {
                "username": "pedro",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )