import uuid
from sqlalchemy import UUID, Column, Float, DateTime
from database.database import Base
import datetime

class FinancialReportModel(Base):
    __tablename__ = 'financial_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    donations = Column(Float, default=0.0)
    sales = Column(Float, default=0.0)
    castrations = Column(Float, default=0.0)
    date_created = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
