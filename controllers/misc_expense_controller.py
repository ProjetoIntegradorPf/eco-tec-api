from flask import Blueprint, jsonify, request
from services.misc_expense_service import (
    list_misc_expenses,
    create_misc_expense_service,
    get_misc_expense_service,
    update_misc_expense_service,
    delete_misc_expense_service
)
from database.database import get_db

misc_expense_bp = Blueprint('misc_expense_bp', __name__)

@misc_expense_bp.route('/misc-expenses', methods=['GET'])
def get_all_misc_expenses():
    db = get_db()
    expenses = list_misc_expenses(db)
    expenses__serialized = [expense.to_dict() for expense in expenses]
    return jsonify(expenses__serialized), 200

@misc_expense_bp.route('/misc-expenses', methods=['POST'])
def create_misc_expense():
    db = get_db()
    expense_data = request.get_json()
    return jsonify(create_misc_expense_service(expense_data, db).to_dict()), 201

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['GET'])
def get_misc_expense(expense_id):
    db = get_db()
    return jsonify(get_misc_expense_service(expense_id, db).to_dict()), 200

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['PUT'])
def update_misc_expense(expense_id):
    db = get_db()
    expense_data = request.get_json()
    update = update_misc_expense_service(expense_id, expense_data, db)
    return jsonify(update.to_dict()), 201

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['DELETE'])
def delete_misc_expense(expense_id):
    db = get_db()
    delete = delete_misc_expense_service(expense_id, db)
    if not delete:
        return jsonify({"detail": "Despesa excluida com sucesso."}), 204
