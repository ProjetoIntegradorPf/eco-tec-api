from models.user_model import UserModel
from sqlalchemy.orm import Session  # Para tipagem correta da sessão

def create_user(db: Session, user: UserModel):
    """
    Cria um novo usuário no banco de dados e retorna o usuário criado.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user  # Adiciona o retorno do usuário

def get_user_by_email(db: Session, email: str):
    """
    Busca um usuário pelo email.
    """

    print("buscando o usuário")
    print(email)
    return db.query(UserModel).filter(UserModel.email == email).first()
