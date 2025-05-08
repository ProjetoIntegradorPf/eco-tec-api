import uuid
from sqlalchemy import UUID, Column, Float, Date
from database.database import Base
import datetime

class ReportModel(Base):
    __tablename__ = 'reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    donation_id = Column(UUID(as_uuid=True))
    donation = Column(Float, default=0)
    cash_donation_id = Column(UUID(as_uuid=True))
    cash_donation = Column(Float, default=0)
    sale_id = Column(UUID(as_uuid=True))
    sale_qtd_sold = Column(Float, default=0)
    sale_value = Column(Float, default=0)
    castration_id = Column(UUID(as_uuid=True))
    castration_value = Column(Float, default=0)
    date_created = Column(Date, default=datetime.datetime.now(datetime.timezone.utc))
    misc_expense_id = Column(UUID(as_uuid=True))
    misc_expense_value = Column(Float, default=0)


    def to_dict(self):
        return {
            "id": str(self.id),
            "donation_id": self.donation_id,
            "donation": self.donation,
            "cash_donation_id": self.cash_donation_id,
            "cash_donation": self.cash_donation,
            "sale_id": self.sale_id,
            "sale_qtd_sold": self.sale_qtd_sold,
            "sale_value": self.sale_value,
            "castration_id": self.castration_id,
            "castration_value": self.castration_value,
            "misc_expense_id": self.misc_expense_id,
            "misc_expense_value": self.misc_expense_value,
            "date_created": self.date_created.isoformat(),
        }
