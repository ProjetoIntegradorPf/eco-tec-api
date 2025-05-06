from flask import Flask
from flask_cors import CORS
from database.database import create_database
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Importar seus blueprints ou rotas
from controllers.user_controller import user_blueprint
from controllers.castration_controller import castration_blueprint
from controllers.donation_controller import donation_blueprint
from controllers.sale_controller import sale_blueprint
from controllers.report_controller import report_blueprint
from controllers.cash_donation_controller import cash_donation_blueprint
from controllers.misc_expense_controller import misc_expense_bp
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
app.register_blueprint(castration_blueprint, url_prefix='/api')
app.register_blueprint(sale_blueprint, url_prefix='/api')
app.register_blueprint(donation_blueprint, url_prefix='/api')
app.register_blueprint(report_blueprint, url_prefix='/api')
app.register_blueprint(cash_donation_blueprint, url_prefix='/api/donations')
app.register_blueprint(misc_expense_bp, url_prefix='/api')
app.register_blueprint(swaggerui_blueprint)

create_database()

if __name__ == "__main__":
    app.run(debug=True)
