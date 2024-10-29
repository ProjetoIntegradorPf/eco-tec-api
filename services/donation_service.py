import datetime
from repositories.donation_repository import (
    create_donation_in_db,
    delete_donation_report, 
    get_donation_by_id as get_donation_by_id_repo, 
    update_donation_in_db, 
    filter_donations,
    delete_donation_repo,
    insert_donation_in_report,
    update_donation_in_report
)
from flask import jsonify

from repositories.report_repository import get_all_financial_reports

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
    donation = create_donation_in_db(donation_data, db, current_user_id)

    if donation:
        insert_donation_in_report(donation, db)

    return donation

def get_donation_by_id(donationId, db):
    # Verificação: doação existe?
    donation = get_donation_by_id_repo(donationId, db)
    if not donation:
        return jsonify({"detail": "Doação não encontrada."}), 404

    return donation

from flask import jsonify
import datetime

def update_donation(donationId, donation_data, db, current_user_id):
    # Verificação: doação existe?
    donation = get_donation_by_id_repo(donationId, db)
    if not donation:
        return jsonify({"detail": "Doação não encontrada."}), 404

    # Validação: verificar se os dados fornecidos são válidos
    if 'quantity' in donation_data and donation_data['quantity'] <= 0:
        return jsonify({"detail": "A quantidade de tampinhas doadas deve ser um número positivo."}), 400

    # Verificação adicional se a quantidade é reduzida
    if donation_data['quantity'] < donation.quantity:
        form_data = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.datetime.today())

        # Inicialização das contagens
        total_donated_caps = 0
        total_sold_caps = 0

        # Cálculo das tampinhas doadas e vendidas
        for form in form_data:
            total_donated_caps += form.donation
            total_sold_caps += form.sale_qtd_sold

        # Tampinhas restantes atualmente no sistema
        current_available_caps = total_donated_caps - donation.quantity 

        current_available_caps += donation_data['quantity']

        # Verificação final: se a nova quantidade resulta em um valor menor do que as vendidas
        if (total_sold_caps > current_available_caps):
            return jsonify({"detail": "Você não pode reduzir essa quantidade de tampinhas, pois ficará menor do que o número de tampinhas já vendidas."}), 400

    # Se passar em todas as validações, atualizar a doação
    updated_donation = update_donation_in_db(donationId, donation_data, db, current_user_id)

    if updated_donation:
        update_donation_in_report(updated_donation, db)

    return jsonify(updated_donation.to_dict()), 200


def delete_donation(donationId, db):
    donation = get_donation_by_id_repo(donationId, db)
    if not donation:
        return jsonify({"detail": "Doação não encontrada."}), 404
    
    form_data = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.datetime.today())

    # Inicialização das contagens
    total_donated_caps = 0
    total_sold_caps = 0

    # Cálculo das tampinhas doadas e vendidas
    for form in form_data:
        total_donated_caps += form.donation
        total_sold_caps += form.sale_qtd_sold

    # Tampinhas restantes atualmente no sistema
    current_available_caps = total_donated_caps - donation.quantity 

    # Verificação final: se a nova quantidade resulta em um valor menor do que as vendidas
    if (total_sold_caps > current_available_caps):
        return jsonify({"detail": "Você não pode excluir, pois ficará menor do que o número de tampinhas já vendidas."}), 400

    delete_donation_report(donationId, db)
    
    delete_donation_repo(donationId, db)

    return None
