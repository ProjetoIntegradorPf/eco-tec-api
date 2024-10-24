from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from database.database import get_db
import services.sale_service as sale_service

sale_blueprint = Blueprint('sale_blueprint', __name__)

@sale_blueprint.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    db: Session = get_db()
    filters = request.args
    sales = sale_service.get_sales(filters, db)

    if isinstance(sales, tuple):
        return sales
    
    sales_serialized = [sale.to_dict() for sale in sales]  # Serializar a lista de vendas
    return jsonify(sales_serialized), 200

@sale_blueprint.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    db: Session = get_db()
    sale_data = request.get_json()
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário logado
    sale = sale_service.create_sale(sale_data, db, current_user_id)

    if isinstance(sale, tuple):
        return sale

    return jsonify(sale.to_dict()), 201

@sale_blueprint.route('/sales/<saleId>', methods=['GET'])
@jwt_required()
def get_sale_by_id(saleId):
    db: Session = get_db()
    current_user_id = get_jwt_identity()
    sale = sale_service.get_sale_by_id(saleId, db, current_user_id)

    if isinstance(sale, tuple):
        return sale

    return jsonify(sale.to_dict()), 200

@sale_blueprint.route('/sales/<saleId>', methods=['PUT'])
@jwt_required()
def update_sale(saleId):
    db: Session = get_db()
    sale_data = request.get_json()
    current_user_id = get_jwt_identity()
    sale = sale_service.update_sale(saleId, sale_data, db, current_user_id)

    if isinstance(sale, tuple):
        return sale

    return jsonify(sale.to_dict()), 200
