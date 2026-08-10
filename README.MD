# Projeto Merchant API

Bem-vindo ao backend do **Projeto Merchant**. Esta é uma API RESTful construída com Django e Django REST Framework, projetada para gerenciar informações de lojistas (merchants)

## ✨ Funcionalidades Principais (Exemplo)

* (Criar, Ler, Atualizar) completo para Lojistas.

## 🚀 Tecnologias Utilizadas

*   **Backend:** Python 3.10, Django, Django REST Framework
*   **Banco de Dados:** PostgreSQL
*   **Gerenciador de Pacotes:** Pip com ambiente virtual Conda
*   **CORS:** django-cors-headers para permitir requisições de diferentes origens

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:

*   Python 3.10
*   Conda (ou qualquer outro gerenciador de ambiente virtual como `venv`)
*   PostgreSQL

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

**1. Clone o Repositório**

```bash
git clone https://github.com/pedro1801/back_end_merchant.git
cd projeto_merchant
```

**2. Crie e Ative o Ambiente Virtual (Conda)**

O comando abaixo criará um ambiente chamado `projetomerchant` com Python 3.10.

```bash
conda create -n projetomerchant python=3.10
conda activate projetomerchant
```

**3. Instale as Dependências**

```bash
 pip install django djangorestframework django-cors-headers psycopg2-binary
```

**4. Configure o Banco de Dados**

Você precisará de um banco de dados PostgreSQL rodando. Crie um banco de dados para este projeto (ex: `merchant_db`).

Depois, configure a conexão no arquivo `projeto_merchant/settings.py`. É altamente recomendado usar variáveis de ambiente para dados sensíveis, mas para um início rápido, você pode editar diretamente:

```python
# projeto_merchant/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'merchant_db',      # Nome do seu banco de dados
        'USER': 'postgres_user',    # Seu usuário do PostgreSQL
        'PASSWORD': 'your_password',# Sua senha
        'HOST': 'localhost',        # Ou o host onde o DB está rodando
        'PORT': '5432',
    }
}
```

**5. Aplique as Migrações**

Este comando criará as tabelas do banco de dados com base nos modelos do Django.

```bash
python manage.py migrate
```

**6. Execute o Servidor de Desenvolvimento**

Tudo pronto! Inicie o servidor.

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

## 📖 Endpoints da API (Exemplo)

Aqui estão alguns exemplos de endpoints que sua API pode ter.

| Endpoint                         | Método  | Descrição                                 |
| -------------------------------- | ------- | ----------------------------------------- |
| `/api/merchants/`                |  `GET`  | Lista todos os lojistas.                  | 
| `/api/merchants/create`          |  `POST` | Cria um novo lojista.                     | 
| `/api/merchants/1/`              |  `GET`  | Obtém detalhes do lojista 1.              | 
| `/api/merchants/status/1`        |  `GET`  | Obtém lojista com status 1.               |
| `/api/merchants/1/update`        |  `PUT`  | Atualiza detalhes do lojista 1.           |
| `/api/merchants/1/update/status` |  `PUT`  | Atualiza status do lojista 1.             |
| `/api/merchants/1/timeline`      |  `GET`  | Pega o timeline do lojista 1.             |
------------------------------------------------------------------------------------------