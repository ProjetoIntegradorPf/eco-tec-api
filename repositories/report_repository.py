from models.report_model import ReportModel
from datetime import datetime

def get_all_financial_reports(db, start_date=None, end_date=None):
    """Retorna todos os relatórios financeiros, com filtros de data opcional."""
    query = db.query(ReportModel)

    if start_date:
        query = query.filter(ReportModel.date_created >= start_date)
    if end_date:
        query = query.filter(ReportModel.date_created <= end_date)

    return query.all()
