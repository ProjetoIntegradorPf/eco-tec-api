import uuid
from sqlalchemy import UUID, Column, String, Integer, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class FinancialReportModel(Base):
    __tablename__ = 'financial_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    total_donations = Column(Float, default=0.0)  # Total de doações (em valor convertido)
    total_sales = Column(Float, default=0.0)  # Total arrecadado nas vendas
    total_spent = Column(Float, default=0.0)  # Total gasto com castrações
    balance = Column(Float, default=0.0)  # Saldo final
    report_date = Column(DateTime, default=datetime.datetime.utcnow)  # Data do relatório
