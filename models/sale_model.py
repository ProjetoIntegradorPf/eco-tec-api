import uuid
from sqlalchemy import UUID, Column, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class SaleModel(Base):
    __tablename__ = 'sales'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    buyer_name = Column(String, index=True)  # Nome do comprador
    sale_date = Column(Date, default=datetime.datetime.now(datetime.timezone.utc))  # Data da doação  # Data da venda
    quantity_sold = Column(Float)  # Quantidade de tampinhas vendidas
    total_value = Column(Float)  # Valor arrecadado com a venda

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Relacionamento com a tabela 'users'
    user = relationship("UserModel", back_populates="sales")

    def to_dict(self):
        return {
            "id": self.id,
            "buyer_name": self.buyer_name,
            "sale_date": self.sale_date.isoformat() if self.sale_date else None,
            "quantity_sold": self.quantity_sold,
            "total_value": self.total_value,
            "user_id": str(self.user_id)
        }
