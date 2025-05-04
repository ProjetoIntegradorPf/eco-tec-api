import uuid
from sqlalchemy import Column, String, DateTime, Date
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID  # Para o tipo UUID no PostgreSQL
import uuid
import datetime
from passlib.hash import bcrypt  # Importando bcrypt corretamente do passlib
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'users'  # Certifique-se de que o nome da tabela está correto

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(Date)
    date_created = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    date_last_updated = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    hashed_password = Column(String)


    donations = relationship("DonationModel", back_populates="user")
    cash_donations = relationship("CashDonationModel", back_populates="user")
    sales = relationship("SaleModel", back_populates="user")
    castrations = relationship("CastrationModel", back_populates="user")


    def verify_password(self, password: str):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        """
        return bcrypt.verify(password, self.hashed_password)  # Usar bcrypt diretamente

    def dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "date_created": self.date_created,
            "date_last_updated": self.date_last_updated
        }
