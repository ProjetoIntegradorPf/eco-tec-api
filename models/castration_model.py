import uuid
from sqlalchemy import UUID, Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class CastrationModel(Base):
    __tablename__ = 'castrations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    animal_name = Column(String, index=True)  # Nome do animal castrado
    clinic_name_or_veterinary_name = Column(String)  # Nome da clínica
    neutering_date = Column(Date, default=datetime.datetime.now(datetime.timezone.utc))  # Data da doação
    cost = Column(Float)  # Custo da castração

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Relacionamento com a tabela 'users'
    user = relationship("UserModel", back_populates="castrations")

    def to_dict(self):
        return {
            "id": self.id,
            "animal_name": self.animal_name,
            "clinic_name_or_veterinary_name": self.clinic_name_or_veterinary_name,
            "neutering_date": self.neutering_date.isoformat() if self.neutering_date else None,
            "cost": self.cost,
            "user_id": str(self.user_id)
        }
