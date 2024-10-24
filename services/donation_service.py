from repositories.donation_repository import (
    create_donation_in_db, 
    get_donation_by_id as get_donation_by_id_repo, 
    update_donation_in_db, 
    filter_donations
)
from flask import jsonify

def get_donations(filters, db):
    return filter_donations(filters, db)

def create_donation(donation_data, db, current_user_id):
    # Validação: verificar se todos os campos obrigatórios estão presentes
    required_fields = ['donor_name', 'donation_date', 'quantity']
    for field in required_fields:
        if field not in donation_data or not donation_data[field]:
            return jsonify({"detail": f"Campo obrigatório '{field}' está ausente ou vazio."}), 400
    
    # Verificar se a quantidade é um número positivo
    if donation_data['quantity'] <= 0:
        return jsonify({"detail": "A quantidade de tampinhas doadas deve ser um número positivo."}), 400

    # Se todas as validações passarem, cria a doação
    return create_donation_in_db(donation_data, db, current_user_id)

def get_donation_by_id(donationId, db, current_user_id):
    # Verificação: doação existe?
    donation = get_donation_by_id_repo(donationId, db)
    if not donation:
        return jsonify({"detail": "Doação não encontrada."}), 404

    return donation

def update_donation(donationId, donation_data, db, current_user_id):
    # Verificação: doação existe?
    donation = get_donation_by_id_repo(donationId, db)
    if not donation:
        return jsonify({"detail": "Doação não encontrada."}), 404

    # Validação: verificar se os dados fornecidos são válidos
    if 'quantity' in donation_data and donation_data['quantity'] <= 0:
        return jsonify({"detail": "A quantidade de tampinhas doadas deve ser um número positivo."}), 400

    # Se passar em todas as validações, atualizar a doação
    updated_donation = update_donation_in_db(donationId, donation_data, db, current_user_id)
    return updated_donation
