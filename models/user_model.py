import uuid
from sqlalchemy import Column, String, DateTime, Date
from database.dateabase import Base
from sqlalchemy.dialects.postgresql import UUID  # Para o tipo UUID no PostgreSQL
import uuid
import datetime
from passlib.hash import bcrypt  # Importando bcrypt corretamente do passlib

class UserModel(Base):
    __tablename__ = 'users'  # Certifique-se de que o nome da tabela está correto

    id = Column(primary_key=True, default=uuid.uuid4, index=True, unique=True)  # UUID como id
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(Date)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    hashed_password = Column(String)

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
