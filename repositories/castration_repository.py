from models.castration_model import CastrationModel
from models.report_model import ReportModel

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
 
def delete_castration_repo(castrationId, db):
    db.query(CastrationModel).filter_by(id=castrationId).delete()
    db.commit()

def insert_castration_in_report(castration, db):
    report = ReportModel()
    report.castration_id = castration.id
    report.castration_value = castration.cost
    report.date_created = castration.neutering_date
    db.add(report)
    db.commit()

def update_castration_in_report(castration, db):
    id = castration.id
    report = db.query(ReportModel).filter_by(castration_id=id).first()
    report.castration_value = castration.cost
    report.date_created = castration.neutering_date
    db.commit()

def delete_castration_report(id, db):
    db.query(ReportModel).filter_by(castration_id=id).delete()
    db.commit()
