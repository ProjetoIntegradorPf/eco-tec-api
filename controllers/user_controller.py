from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import UserModel
import schemas.user_schema as user_schemas
import services.user_service as user_service

# Definir o Blueprint
user_blueprint = Blueprint('user_blueprint', __name__)

# Criando uma lista de tokens revogados
token_blocklist = set()

# Rota para criar um novo usuário
@user_blueprint.route('/users', methods=['POST'])
def create_user():
    db: Session = get_db()

    # Recebe os dados do JSON da requisição
    user_data = request.get_json()
    user_schema = user_schemas.UserCreateSchema(**user_data)

    db_user = user_service.get_user_by_email(user_schema.email, db)
    if db_user:
        return jsonify({"detail": "Email already in use"}), 400

    # Cria um novo usuário usando o service
    new_user = user_service.create_user(user_schema, db)

    return jsonify(new_user.dict()), 201


# Rota para geração de token JWT
@user_blueprint.route('/token', methods=['POST'])
def generate_token():
    db: Session = get_db()

    form_data = request.get_json()
    if not form_data:
        return jsonify({"detail": "Invalid request, JSON data expected"}), 400
    
    username = form_data.get('username')
    password = form_data.get('hashed_password')

    user = user_service.authenticate_user(username, password, db)

    if not user:
        return jsonify({"detail": "Invalid Credentials"}), 401

    # Definindo a validade do token para 1 hora
    expires = timedelta(hours=1)

    # Cria um novo token JWT para o usuário autenticado com expiração
    token = create_access_token(identity=user.id, expires_delta=expires)
    
    return jsonify(access_token=token), 200

# Rota protegida para obter os dados do usuário atual
@user_blueprint.route('/users/me', methods=['GET'])
@jwt_required()
def get_user():
    db: Session = get_db()

    # Obtém o id do usuário atual a partir do token JWT
    current_user_id = get_jwt_identity()
    user = db.query(UserModel).get(current_user_id)

    if user is None:
        return jsonify({"detail": "User not found"}), 404

    # Converte o modelo de usuário para o schema
    user_schema = user_schemas.UserSchema.model_validate(user)

    # Aqui o 'model_dump' não precisa de parâmetros adicionais
    return jsonify(user_schema.model_dump())

# Função para revogar o token anterior
def revoke_token(jti):
    token_blocklist.add(jti)

# Rota para efetuar logout e revogar o token atual
@user_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Recupera o JTI do token atual
    revoke_token(jti)       # Adiciona o JTI à blocklist
    return jsonify(msg="Logout realizado com sucesso. Token revogado."), 200
