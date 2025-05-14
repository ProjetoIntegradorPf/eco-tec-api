from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

from database.database import Base
class MiscExpenseModel(Base):
    __tablename__ = "misc_expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    expense_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "expense_date": self.expense_date,
            "value": self.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }