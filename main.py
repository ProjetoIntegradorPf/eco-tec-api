from flask import Flask
from flask_cors import CORS
from database.dateabase import create_database
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Importar seus blueprints ou rotas
from controllers.user_controller import user_blueprint

# Inicializar a aplicação Flask
app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL onde o Swagger UI será acessado

# Caminho para o arquivo swagger.yaml ou swagger.json
API_URL = '/static/swagger.yaml'  # Certifique-se de que o arquivo está em "static/swagger.yaml"

# Configurando o Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,            # URL onde o Swagger será exibido
    API_URL              # URL para o arquivo Swagger (YAML/JSON)
)

app.config['JWT_SECRET_KEY'] = 'myjwtsecret'  # Mantenha essa chave segura

jwt = JWTManager(app)

# Habilitar CORS
CORS(app)

# Registrar os blueprints
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(swaggerui_blueprint)

# Criar o banco de dados
create_database()

if __name__ == "__main__":
    app.run(debug=True)
