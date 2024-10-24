from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session
from database.database import get_db
import services.donation_service as donation_service

donation_blueprint = Blueprint('donation_blueprint', __name__)

# Rota para listar doações
@donation_blueprint.route('/donations', methods=['GET'])
@jwt_required()
def get_donations():
    db: Session = get_db()
    filters = request.args
    donations = donation_service.get_donations(filters, db)

    # Serializando cada doação para um dicionário
    donations_serialized = [donation.to_dict() for donation in donations]

    return jsonify(donations_serialized), 200


# Rota para criar uma nova doação
@donation_blueprint.route('/donations', methods=['POST'])
@jwt_required()
def create_donation():
    db: Session = get_db()
    donation_data = request.get_json()

    current_user_id = get_jwt_identity()

    # Criando a doação via service
    donation = donation_service.create_donation(donation_data, db, current_user_id)

    # Verificando se houve erro ao criar a doação
    if isinstance(donation, tuple) and donation[1] == 400:
        return donation  # Retorna o erro caso haja problema nos dados

    return jsonify(donation.to_dict()), 201


# Rota para obter uma doação específica
@donation_blueprint.route('/donations/<donationId>', methods=['GET'])
@jwt_required()
def get_donation_by_id(donationId):
    db: Session = get_db()

    donation = donation_service.get_donation_by_id(donationId, db)

    # Verificando se a doação foi encontrada ou se houve erro de permissão
    if isinstance(donation, tuple):
        return donation  # Retorna o erro apropriado

    return jsonify(donation.to_dict()), 200


# Rota para atualizar uma doação existente
@donation_blueprint.route('/donations/<donationId>', methods=['PUT'])
@jwt_required()
def update_donation(donationId):
    db: Session = get_db()
    donation_data = request.get_json()
    current_user_id = get_jwt_identity()

    donation = donation_service.update_donation(donationId, donation_data, db, current_user_id)

    # Verificando se a doação foi encontrada, ou se houve erro de permissão ou validação
    if isinstance(donation, tuple):
        return donation  # Retorna o erro apropriado

    return jsonify(donation.to_dict()), 200

@donation_blueprint.route('/donations/<donationId>', methods=['DELETE'])
@jwt_required()
def delete_donation(donationId):
    db: Session = get_db()
    # Obtém a castração e verifica se o usuário tem permissão para visualizar
    donation = donation_service.delete_donation(donationId, db)

    # Retorna erro se a castração não for encontrada ou se o usuário não tiver permissão
    if isinstance(donation, tuple):
        return donation

    return jsonify(donation), 200