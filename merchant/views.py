from django.db import OperationalError
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status

from .models import Merchant, StatusMerchant, MerchantStatusHistory
import merchant.serializers as serializers


class MerchantCreateView(APIView):

    def get(self, request):
        return Response(
            {
                "cnpj": "string",
                "razao_social": "string",
                "nome_fantasia": "string",
                "email": "string",
                "telefone": "string",
                "status_id": "int"
            } 
        )

    def post(self, request):
        try:
            draft_status = StatusMerchant.objects.get(status_name="draft")

            serializer = serializers.MerchantSerializerCreate(data=request.data)
            if serializer.is_valid():
                serializer.save(status=draft_status)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantListView(APIView):

    def get(self, request):
        try:
            merchants = Merchant.objects.all()

            if not merchants.exists():
                raise NotFound(
                    "Merchants não encontrados"
                )

            serializer = serializers.MerchantSerializer(
                merchants,
                many=True
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantIdView(APIView):

    def get(self, request, merchant_id):
        try:
            merchant = Merchant.objects.filter(id=merchant_id).first()

            if not merchant:
                raise NotFound(
                    "Merchant não encontrado"
                )

            serializer = serializers.MerchantSerializer(merchant)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantStatusView(APIView):
    
    def get(self, request, status_id):
        try:
            merchants = Merchant.objects.filter(status_id=status_id).select_related("status")

            if not merchants.exists():
                raise NotFound(
                    "Merchants não encontrados para o status fornecido"
                )
            serializer = serializers.MerchantSerializer(
                merchants,
                many=True
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantUpdateView(MerchantIdView):

    def put(self, request, merchant_id):
        try:
            merchant = Merchant.objects.filter(id=merchant_id).first()

            if not merchant:
                raise NotFound(
                    "Merchant não encontrado"
                )
            
            if merchant.status.status_name != "draft":
                return Response(
                    {
                        "detail": "Apenas merchants com status 'draft' podem ser atualizados."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = serializers.MerchantSerializerUpdate(
                merchant,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantUpdataStatusView(APIView):

    def salvar_historico_status(self,merchant,status_anterior,values):
        historico = serializers.MerchantStatusHistorySerializer(
            data={
                "id_merchant": merchant.id,
                "id_usuario": values["user_id"].id,
                "status_anterior": status_anterior.id if status_anterior else None,
                "motivo": values.get("motivo")
            }
        )

        historico.is_valid(raise_exception=True)
        historico.save()

    def get(self, request, merchant_id):
        return Response(
            {
                "user_id": "Codigo do Usuário",
                "status": "Codigo do Status",
                "motivo": "string"
            } 
        )
    
    def put(self, request, merchant_id):


        try:
            merchant = Merchant.objects.filter(id=merchant_id).first()
            new_status = StatusMerchant.objects.filter(id=request.data["status"]).first()
            if not new_status:
                return Response(
                    {
                        "detail": "Status não encontrado"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not merchant:
                raise NotFound("Merchant não encontrado.")

            motivo = request.data.get("motivo")
            status_atual = merchant.status.status_name
            status_novo = new_status.status_name
            transicoes_permitidas = {
                ("draft", "pending_analysis"): "alterado para pending_analysis",
                ("pending_analysis", "approved"): "alterado para approved",
                ("pending_analysis", "rejected"): "alterado para rejected",
                ("approved", "blocked"): "alterado para blocked",
            }

            transicao = (status_atual, status_novo)

            if transicao not in transicoes_permitidas:
                return Response(
                    {
                        "detail": f"Transicao não permitida de {status_atual} para {status_novo}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            transicoes_com_motivo_obrigatorio = {
                ("pending_analysis", "rejected"),
                ("approved", "blocked"),
            }

            if transicao in transicoes_com_motivo_obrigatorio and motivo is None:
                return Response(
                    {
                        "detail": "Motivo Obrigatorio"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if motivo is None:
                request.data["motivo"] = f"{status_atual} para {status_novo}"

            detal = transicoes_permitidas[transicao]

            serializer = serializers.MerchantUpdateStatusSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)
            values = serializer.validated_data

            status_anterior = merchant.status

            merchant.status = values["status"]
            merchant.save(update_fields=["status"])

            self.salvar_historico_status(
                merchant=merchant,
                status_anterior=status_anterior,
                values=values
            )

            return Response(
                {
                    "detail": detal,
                    "merchant_id": merchant.id,
                    "status": merchant.status_id
                },
                status=status.HTTP_200_OK
            )

        except OperationalError:
            return Response(
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MerchantTimeLineListView(APIView):

    def get(self, request, merchant_id):
        try:
            merchant = Merchant.objects.filter(id=merchant_id).first()

            if not merchant:
                raise NotFound("Merchant não encontrado.")

            historico = MerchantStatusHistory.objects.filter(
                id_merchant_id=merchant_id
            ).select_related(
                "id_merchant",
                "status_anterior",
            )

            serializer = serializers.MerchantTimeLineView(
                historico,
                many=True
            )

            return Response(serializer.data)

        except OperationalError:
            return Response (
                {
                    "detail": "Erro ao acessar o banco de dados."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {
                    "detail": "Usuário ou senha inválidos"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "detail": "Login realizado com sucesso",
                "user_id": user.id,
                "username": user.username
            },
            status=status.HTTP_200_OK
        )