from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from database.database import get_db
import services.castration_service as castration_service

castration_blueprint = Blueprint('castration_blueprint', __name__)

# Rota para listar castrações com filtros opcionais
@castration_blueprint.route('/castrations', methods=['GET'])
@jwt_required()
def get_castrations():
    db: Session = get_db()
    filters = request.args
    castrations = castration_service.get_castrations(filters, db)

    # Serializando as castrações em uma lista de dicionários
    castrations_serialized = [castration.to_dict() for castration in castrations]

    return jsonify(castrations_serialized), 200


# Rota para criar uma nova castração
@castration_blueprint.route('/castrations', methods=['POST'])
@jwt_required()
def create_castration():
    db: Session = get_db()
    castration_data = request.get_json()
    current_user_id = get_jwt_identity()  # Para associar a castração ao usuário que criou

    # Cria a castração no banco de dados
    castration = castration_service.create_castration(castration_data, db, current_user_id)

    # Validação: retorna erro se houver algum problema ao criar a castração
    if isinstance(castration, tuple) and castration[1] == 400:
        return castration

    return jsonify(castration.to_dict()), 201


# Rota para obter uma castração específica
@castration_blueprint.route('/castrations/<castrationId>', methods=['GET'])
@jwt_required()
def get_castration_by_id(castrationId):
    db: Session = get_db()
    current_user_id = get_jwt_identity()

    # Obtém a castração e verifica se o usuário tem permissão para visualizar
    castration = castration_service.get_castration_by_id(castrationId, db, current_user_id)

    # Retorna erro se a castração não for encontrada ou se o usuário não tiver permissão
    if isinstance(castration, tuple):
        return castration

    return jsonify(castration.to_dict()), 200


# Rota para atualizar uma castração existente
@castration_blueprint.route('/castrations/<castrationId>', methods=['PUT'])
@jwt_required()
def update_castration(castrationId):
    db: Session = get_db()
    castration_data = request.get_json()
    current_user_id = get_jwt_identity()

    # Atualiza a castração e valida erros
    castration = castration_service.update_castration(castrationId, castration_data, db, current_user_id)

    # Retorna erro se a castração não for encontrada ou se o usuário não tiver permissão
    if isinstance(castration, tuple):
        return castration

    return jsonify(castration.to_dict()), 200
