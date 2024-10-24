
# API de Gestão de ONG

## Descrição

Esta API foi desenvolvida para o gerenciamento de uma ONG, permitindo o controle de usuários, doações, vendas e castrações. A aplicação usa autenticação JWT para proteger os endpoints e garantir o acesso seguro às informações.

## Tecnologias

- **Flask** - Framework para desenvolvimento da API.
- **SQLAlchemy** - ORM para interação com o banco de dados.
- **PostgreSQL** - Banco de dados utilizado.
- **Docker** e **Docker Compose** - Para gerenciamento e execução de serviços.
- **JWT** - Para autenticação e autorização.

## Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.x instalado.

## Configuração do Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ProjetoIntegradorPf/eco-tec-api.git
   cd eco-tec-api
   ```

## Como rodar o projeto

### Passo 1: Subir os serviços com Docker Compose

Antes de rodar a aplicação Flask, é necessário iniciar os serviços com o Docker Compose. Isso garantirá que o banco de dados e outros serviços necessários estejam em execução.

1. **Iniciar os serviços com Docker Compose:**

   Execute o seguinte comando na raiz do projeto para subir o banco de dados e outros serviços necessários:

   ```bash
   docker-compose up -d
   ```

   Este comando iniciará os contêineres no modo _detached_, o que significa que eles rodarão em segundo plano.

2. **Verificar se os serviços estão ativos:**

   Para verificar se os contêineres estão rodando corretamente, execute:

   ```bash
   docker-compose ps
   ```

   Isso listará os contêineres ativos, incluindo o banco de dados PostgreSQL.

### Passo 2: Rodar a aplicação Flask

Após o Docker Compose subir os serviços necessários (como o banco de dados), você pode iniciar a aplicação Flask.

1. **Ativar o ambiente virtual (opcional):**

   Se estiver usando um ambiente virtual, ative-o:

   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

2. **Instalar as dependências:**

   Caso ainda não tenha instalado as dependências do projeto, faça isso agora:

   ```bash
   pip install -r requirements.txt
   ```

3. **Rodar a aplicação:**

   Com todos os serviços ativos, inicie a aplicação Flask:

   ```bash
   python main.py
   ```

   A aplicação estará disponível em `http://localhost:5000/api`.

## Testando a API

A API pode ser testada manualmente ou utilizando ferramentas como o [Postman](https://www.postman.com) ou o [Swagger UI](http://localhost:5000/swagger).

1. **Documentação da API:**

   A API segue o padrão OpenAPI 3.0. A documentação pode ser acessada via Swagger UI em:

   ```
   http://localhost:5000/api/docs
   ```

## Finalizando os serviços

Quando terminar de usar a aplicação, você pode parar e remover os contêineres com o seguinte comando:

```bash
docker-compose down
```

Isso encerrará todos os serviços associados ao Docker Compose.

## Contato

Para dúvidas ou sugestões, entre em contato com [projeto.integrador.pf@gmail.com](mailto:projeto.integrador.pf@gmail.com).
