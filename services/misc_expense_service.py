from flask import jsonify

from repositories.misc_expense_repository import (
    create_misc_expense,
    get_misc_expense_by_id,
    update_misc_expense,
    delete_misc_expense,
    filter_misc_expenses,
    insert_misc_expense_in_report,
    update_misc_expense_in_report,
    delete_misc_expense_from_report
)

def list_misc_expenses(filters, db):
    return filter_misc_expenses(filters, db)

def create_misc_expense_service(expense_data, db):
    if 'description' not in expense_data or not expense_data['description']:
        return jsonify({"detail": "Campo obrigatório 'description' está ausente ou vazio."}), 400
    if 'value' not in expense_data or expense_data['value'] <= 0:
        return jsonify({"detail": "O valor da despesa deve ser positivo."}), 400

    expense = create_misc_expense(expense_data, db)
    insert_misc_expense_in_report(expense, db)
    return jsonify(expense.to_dict()), 201

def get_misc_expense_service(expense_id, db):
    expense = get_misc_expense_by_id(expense_id, db)
    if not expense:
        return jsonify({"detail": "Despesa não encontrada."}), 404
    return jsonify(expense.to_dict())

def update_misc_expense_service(expense_id, expense_data, db):
    updated = update_misc_expense(expense_id, expense_data, db)
    if not updated:
        return jsonify({"detail": "Despesa não encontrada."}), 404
    update_misc_expense_in_report(updated, db)
    return jsonify(updated.to_dict())

def delete_misc_expense_service(expense_id, db):
    expense = get_misc_expense_by_id(expense_id, db)
    if not expense:
        return jsonify({"detail": "Despesa não encontrada."}), 404
    delete_misc_expense_from_report(expense_id, db)
    delete_misc_expense(expense_id, db)
    return '', 204
