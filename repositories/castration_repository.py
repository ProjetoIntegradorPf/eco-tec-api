from models.castration_model import CastrationModel

def create_castration_in_db(castration_data, db, current_user_id):
    castration = CastrationModel(**castration_data)
    castration.user_id = current_user_id
    db.add(castration)
    db.commit()
    return castration

def get_castration_by_id(castrationId, db):
    return db.query(CastrationModel).get(castrationId)

def update_castration_in_db(castrationId, castration_data, db, current_user_id):
    castration = get_castration_by_id(castrationId, db)
    if castration:
        for key, value in castration_data.items():
            setattr(castration, key, value)

        castration.user_id = current_user_id
        db.commit()
    return castration

def filter_castrations(filters, db):
    query = db.query(CastrationModel)
    if filters.get('animal_name'):
        query = query.filter(CastrationModel.animal_name == filters['animal_name'])
    # Adicione outros filtros
    return query.all()
