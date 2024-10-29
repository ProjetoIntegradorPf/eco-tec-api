from repositories.report_repository import get_all_financial_reports
from datetime import datetime

def fetch_all_financial_reports(db, start_date_str=None, end_date_str=None):
    """Busca todos os relatórios financeiros, com filtros opcionais de data."""
    start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
    end_date = datetime.fromisoformat(end_date_str) if end_date_str else None

    return get_all_financial_reports(db, start_date=start_date, end_date=end_date)
