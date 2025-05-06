from flask import Blueprint, request
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
    filters = request.args.to_dict()
    return list_misc_expenses(filters, db)

@misc_expense_bp.route('/misc-expenses', methods=['POST'])
def create_misc_expense():
    db = get_db()
    expense_data = request.get_json()
    return create_misc_expense_service(expense_data, db)

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['GET'])
def get_misc_expense(expense_id):
    db = get_db()
    return get_misc_expense_service(expense_id, db)

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['PUT'])
def update_misc_expense(expense_id):
    db = get_db()
    expense_data = request.get_json()
    return update_misc_expense_service(expense_id, expense_data, db)

@misc_expense_bp.route('/misc-expenses/<expense_id>', methods=['DELETE'])
def delete_misc_expense(expense_id):
    db = get_db()
    return delete_misc_expense_service(expense_id, db)
