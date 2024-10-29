from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from database.database import get_db
import services.report_service as report_service

report_blueprint = Blueprint('report_blueprint', __name__)

@report_blueprint.route('/reports', methods=['GET'])
@jwt_required()
def get_all_financial_reports():
    """Endpoint para obter todos os relatórios financeiros, com filtros opcionais de data."""
    db: Session = get_db()

    # Capturar parâmetros de data da query string
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Chamar o serviço com os filtros de data
    reports = report_service.fetch_all_financial_reports(db, start_date, end_date)
    reports_serialized = [report.to_dict() for report in reports]  # Converter para dicionário para serialização
    return jsonify(reports_serialized), 200
