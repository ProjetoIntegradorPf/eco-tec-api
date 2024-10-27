from models.user_model import UserModel

def create_initial_user(db):
    user_data = {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "first_name": "Admin",
        "last_name": "",
        "email": "admin@admin.com",
        "date_of_birth": "1990-07-08",
        "hashed_password": "$2b$12$2zpMbCttatSAoA.skwyD9u7SOGVYKsmN5/VHIv4xA7hcvRMAFiDS."
    }

    user = UserModel(**user_data.dict())

    db.add(user)
    db.commit()
    db.close()
