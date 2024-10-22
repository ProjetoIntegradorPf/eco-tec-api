from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuração do banco de dados
DATABASE_URL = "postgresql://eco-tec-api-user:password@localhost:5439/eco-tec-api-user"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def create_database():
    """
    Função para criar todas as tabelas no banco de dados com base nos modelos.
    """
    from models.user_model import UserModel  # Certifique-se de que o modelo está sendo importado
    print("Tentando criar tabelas...")
    
    # Print para verificar quais tabelas SQLAlchemy conhece
    print("Tabelas registradas:", Base.metadata.tables.keys())

    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")




def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()  # Create a new session
    try:
        return db  # Return the session directly
    finally:
        db.close()  # Close the session after use
