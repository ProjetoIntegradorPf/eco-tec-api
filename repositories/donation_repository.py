from models.donation_model import DonationModel
from models.report_model import ReportModel

def create_donation_in_db(donation_data, db, current_user_id):

    donation = DonationModel(**donation_data)
    donation.user_id = current_user_id
    db.add(donation)
    db.commit()
    return donation

def get_donation_by_id(donationId, db):
    return db.query(DonationModel).get(donationId)

def update_donation_in_db(donationId, donation_data, db, current_user_id):
    # Buscar a doação existente pelo ID
    donation = get_donation_by_id(donationId, db)
    
    if donation:
        # Atualizar os campos da doação, exceto o `user_id`
        for key, value in donation_data.items():
            if value is not None:  # Atualiza apenas valores não nulos
                setattr(donation, key, value)

        # Atualizar o campo `user_id` para o ID do usuário que está realizando o update
        donation.user_id = current_user_id

        db.commit()  # Salvar as alterações no banco de dados
        return donation
    return None
  

def filter_donations(filters, db):
    query = db.query(DonationModel)
    if filters.get('donor_name'):
        query = query.filter(DonationModel.donor_name == filters['donor_name'])
    # Adicione outros filtros
    return query.all()

def delete_donation_repo(donationId, db):
    db.query(DonationModel).filter_by(id=donationId).delete()
    db.commit()

def insert_donation_in_report(donation, db):
    report = ReportModel()
    report.donation_id = donation.id
    report.donation = donation.quantity
    report.date_created = donation.donation_date
    db.add(report)
    db.commit()

def update_donation_in_report(donation, db):
    report = db.query(ReportModel).filter_by(donation_id=donation.id).first()
    report.donation = donation.quantity
    report.date_created = donation.donation_date
    db.commit()

def delete_donation_report(id, db):
    db.query(ReportModel).filter_by(donation_id=id).delete()
    db.commit()