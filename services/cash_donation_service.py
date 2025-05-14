import datetime
from flask import jsonify

from repositories.cash_donation_repository import (
    create_cash_donation_in_db,
    get_cash_donation_by_id,
    update_cash_donation_in_db,
    delete_cash_donation_repo,
    filter_cash_donations,
    insert_cash_donation_in_report,
    update_cash_donation_in_report,
    delete_cash_donation_report
)

from repositories.report_repository import get_all_financial_reports

def get_cash_donations(filters, db):
    return filter_cash_donations(filters, db)

def create_cash_donation(donation_data, db, current_user_id):
    required_fields = ['donor_name', 'donation_date', 'quantity']
    for field in required_fields:
        if field not in donation_data or not donation_data[field]:
            return jsonify({"detail": f"Campo obrigatório '{field}' está ausente ou vazio."}), 400

    if donation_data['quantity'] <= 0:
        return jsonify({"detail": "A quantia de dinheiro doado deve ser um número positivo."}), 400

    donation = create_cash_donation_in_db(donation_data, db, current_user_id)

    if donation:
        insert_cash_donation_in_report(donation, db)

    return donation

def get_cash_donation_by_id(donation_id, db):
    donation = get_cash_donation_by_id(donation_id, db)
    if not donation:
        return jsonify({"detail": "Doação em dinheiro não encontrada."}), 404

    return donation

def update_cash_donation(donation_id, donation_data, db, current_user_id):
    donation = get_cash_donation_by_id(donation_id, db)
    if not donation:
        return jsonify({"detail": "Doação em dinheiro não encontrada."}), 404

    if (None != donation_data['quantity']) and donation_data['quantity'] <= 0:
        return jsonify({"detail": "A quantia de dinheiro doado deve ser um número positivo."}), 400

    if donation_data['quantity'] < donation.quantity:
        financial_reports = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.datetime.today())

        total_donated_money = sum(report.cash_donation for report in financial_reports)
        total_donated_money += sum(report.donation for report in financial_reports)
        total_spent_money = sum(report.spent_value for report in financial_reports)

        available_money = total_donated_money - donation.quantity + donation_data['quantity']

        if total_spent_money > available_money:
            return jsonify({"detail": "Você não pode reduzir esse valor, pois ficaria menor do que o montante já gasto."}), 400

    updated_donation = update_cash_donation_in_db(donation_id, donation_data, db, current_user_id)

    if updated_donation:
        update_cash_donation_in_report(updated_donation, db)

    return updated_donation

def delete_cash_donation(donation_id, db):
    donation = get_cash_donation_by_id(donation_id, db)
    if not donation:
        return jsonify({"detail": "Doação em dinheiro não encontrada."}), 404

    financial_reports = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.datetime.today())

    total_donated_money = sum(report.donation for report in financial_reports)
    total_donated_money += sum(report.cash_donation for report in financial_reports)
    total_spent_money = sum(report.spent_value for report in financial_reports)

    available_money = total_donated_money - donation.quantity

    if total_spent_money > available_money:
        return jsonify({"detail": "Você não pode excluir essa doação, pois o valor restante ficaria menor do que o montante já gasto."}), 400

    delete_cash_donation_repo(donation_id, db)
    delete_cash_donation_report(donation_id, db)

    return None
