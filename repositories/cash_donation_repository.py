from models.cash_donation_model import CashDonationModel
from models.report_model import ReportModel

def create_cash_donation_in_db(donation_data, db, current_user_id):
    donation = CashDonationModel(**donation_data)
    donation.user_id = current_user_id
    db.add(donation)
    db.commit()
    return donation

def get_cash_donation_by_id(donation_id, db):
    return db.query(CashDonationModel).get(donation_id)

def update_cash_donation_in_db(donation_id, donation_data, db, current_user_id):
    donation = get_cash_donation_by_id(donation_id, db)
    
    if donation:
        for key, value in donation_data.items():
            if value is not None:
                setattr(donation, key, value)

        donation.user_id = current_user_id
        db.commit()
        return donation
    return None

def filter_cash_donations(filters, db):
    query = db.query(CashDonationModel)
    if filters.get('donor_name'):
        query = query.filter(CashDonationModel.donor_name == filters['donor_name'])
    # Adicione outros filtros conforme necessário
    return query.all()

def delete_cash_donation_repo(donation_id, db):
    db.query(CashDonationModel).filter_by(id=donation_id).delete()
    db.commit()

def insert_cash_donation_in_report(donation, db):
    report = ReportModel()
    report.cash_donation_id = donation.id
    report.cash_donationdonation = donation.quantity
    report.date_created = donation.donation_date
    db.add(report)
    db.commit()

def update_cash_donation_in_report(donation, db):
    report = db.query(ReportModel).filter_by(donation_id=donation.id).first()
    if report:
        report.cash_donation = donation.quantity
        report.date_created = donation.donation_date
        db.commit()

def delete_cash_donation_report(donation_id, db):
    db.query(ReportModel).filter_by(cash_donation_id=donation_id).delete()
    db.commit()
