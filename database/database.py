from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuração do banco de dados
DATABASE_URL = "postgresql://eco_tec_9u95_user:J7gl3ZqvIMu4V8LIrNl2cDbbMRNvTxzM@dpg-d0eh1s49c44c73832glg-a.oregon-postgres.render.com/eco_tec_9u95"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def create_database():
    """
    Função para criar todas as tabelas no banco de dados com base nos modelos.
    """
    from models.user_model import UserModel  # Certifique-se de que o modelo está sendo importado
    from models.donation_model import DonationModel
    from models.report_model import ReportModel
    from models.castration_model import CastrationModel
    from models.sale_model import SaleModel
    from models.cash_donation_model import CashDonationModel   
    from models.misc_expense_model import MiscExpenseModel 
    
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()  # Create a new session
    try:
        return db  # Return the session directly
    finally:
        db.close()  # Close the session after use
