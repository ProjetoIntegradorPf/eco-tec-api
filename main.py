from flask import Flask
from flask_cors import CORS
from database.dateabase import create_database
from flask_jwt_extended import JWTManager

# Importar seus blueprints ou rotas
from controllers.user_controller import user_blueprint

# Inicializar a aplicação Flask
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'myjwtsecret'  # Mantenha essa chave segura

jwt = JWTManager(app)

# Habilitar CORS
CORS(app)

# Registrar os blueprints
app.register_blueprint(user_blueprint, url_prefix='/api')

# Criar o banco de dados
create_database()

if __name__ == "__main__":
    app.run(debug=True)
