import uuid
from sqlalchemy import UUID, Column, String, Integer, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base
import datetime


class DonationModel(Base):
    __tablename__ = 'donations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    donor_name = Column(String, index=True)  # Nome do doador
    donation_date = Column(Date, default=datetime.datetime.now(datetime.timezone.utc))  # Data da doação
    quantity = Column(Float)  # Quantidade de tampinhas doadas

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Relacionamento com a tabela 'users'
    user = relationship("UserModel", back_populates="donations")


    def to_dict(self):
        return {
            'id': self.id,
            'donor_name': self.donor_name,
            'donation_date': self.donation_date.isoformat() if self.donation_date else None,
            'quantity': self.quantity,
            'user_id': self.user_id
        }