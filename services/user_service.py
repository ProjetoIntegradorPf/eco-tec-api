from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import jwt as _jwt
import sqlalchemy.orm as orm
import passlib.hash as hash
from models.user_model import UserModel
import repositories.user_repository as user_repository
import schemas.user_schema as user_schema

# Configuração da aplicação Flask
app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = "myjwtsecret"
jwt = JWTManager(app)


# Funções adaptadas de FastAPI para Flask

def get_user_by_email(email: str, db: orm.Session):
    """
    Busca um usuário pelo e-mail.
    """
    return user_repository.get_user_by_email(db, email)


def create_user(user: user_schema.UserCreateSchema, db: orm.Session):
    """
    Cria um novo usuário com a senha hash.
    """
    user_obj = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        email=user.email,
        hashed_password=hash.bcrypt.hash(user.hashed_password)  # Hash da senha
    )
    user_repository.create_user(db=db, user=user_obj)
    return user_obj


def authenticate_user(email: str, password: str, db: orm.Session):
    """
    Autentica um usuário baseado no e-mail e senha.
    """
    user = get_user_by_email(email, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


def create_token(user: UserModel):
    """
    Gera um token JWT para o usuário autenticado.
    """
    user_obj = user_schema.UserSchema.from_orm(user)
    token = create_access_token(identity=user.id)  # Usa o ID do usuário como identidade
    return {"access_token": token, "token_type": "bearer"}


@jwt_required()  # Exige o JWT para acessar
def get_current_user(db: orm.Session):
    """
    Obtém o usuário atual a partir do JWT.
    """
    user_id = get_jwt_identity()  # Obtém o ID do usuário a partir do token
    user = db.query(UserModel).get(user_id)
    
    if user is None:
        return jsonify({"detail": "User not found"}), 404

    return user
