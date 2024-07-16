# Terra-Tech-api

Bem-vindo ao Terra-Tech-api, uma API desenvolvida para análise da folha do café, com funcionalidades de autenticação robusta. Este projeto utiliza Python, Django e MariaDB.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.9+
- **Framework**: Django 3.2+
- **Banco de Dados**: MariaDB
- **Autenticação**: JSON Web Tokens (JWT) com django-rest-knox 

## Funcionalidades

### Autenticação

- **Registro de Usuário**: Permite que novos usuários se registrem fornecendo informações básicas.
- **Login**: Sistema de login que permite aos usuários acessarem a API com credenciais válidas.
- **Autenticação JWT**: Utiliza JWT para autenticação segura e gerenciamento de sessões.
- **Recuperação de Senha**: Permite que os usuários redefinam suas senhas através de e-mail.

### Análise da Folha do Café

- **Upload de Imagens**: Permite que os usuários façam upload de imagens das folhas de café.
- **Processamento de Imagens**: Algoritmos para análise das imagens enviadas, identificando características relevantes (doenças, pragas, etc.).
- **Relatórios de Análise**: Gera relatórios detalhados com os resultados da análise das folhas de café, incluindo sugestões de tratamento.
- **Histórico de Análises**: Mantém um histórico das análises realizadas por cada usuário, permitindo acesso fácil a dados anteriores.

## Configuração do Projeto

### Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

- Python 3.9+
- MariaDB
- Virtualenv (opcional, mas recomendado)

### Passos para Configuração

1. **Clone o repositório:**

   ```sh
   git clone https://github.com/seu-usuario/Terra-Tech-api.git
   cd Terra-Tech-api

2. **Crie e ative um ambiente virtual:**

  ```sh
  python -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  ```
3. **Instale as dependências:**

```sh
  pip install -r requirements.txt
```
4. **Configuração do Banco de Dados:**

Configure seu banco de dados MariaDB e atualize as configurações no arquivo settings.py:

```python

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'nome_do_banco_de_dados',
          'USER': 'seu_usuario',
          'PASSWORD': 'sua_senha',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
```
5. ***Migrações do Banco de Dados:**

Aplique as migrações para criar as tabelas no banco de dados:

```sh

  python manage.py migrate
  Criação de Superusuário:
```
6. **Crie um superusuário para acessar a administração do Django:**

```sh
 
  python manage.py createsuperuser

```

7. ** Execução do Servidor:**
   Inicie o servidor de desenvolvimento:

  ```sh
    python manage.py runserver
    A API estará disponível em http://127.0.0.1:8000/.
  ```
## Endpoints Principais

### Autenticação

- `POST /api-auth/` - Inclui URLs de autenticação da Django Rest Framework
- `GET /activate/<str:token>/` - Ativação de conta
- `POST /forgot-password/` - Recuperação de senha
- `POST /verify-token/` - Verificação de token
- `POST /reset-password/` - Redefinição de senha
- `POST /create-user/` - Criação de usuário
- `PUT /update-user/<int:pk>/` - Atualização de usuário
- `POST /login/` - Login de usuário
- `POST /logout/` - Logout de usuário
- `POST /logout-all/` - Logout de todos os dispositivos

### Análise de Imagens

- `POST /photos` - Upload de fotos
- `DELETE /photos/<int:pk>` - Deletar foto
- `GET /photos/` - Listar fotos
- `GET /photos/filter/` - Filtrar fotos

### Outros

- `POST /` - Upload geral
- `GET /download/` - Download de arquivos

## Contribuição

Sinta-se à vontade para contribuir com o projeto enviando pull requests. Toda ajuda é bem-vinda!

