from models.report_model import ReportModel
from models.sale_model import SaleModel

def create_sale_in_db(sale_data, db, current_user_id):
    sale = SaleModel(**sale_data)
    sale.user_id = current_user_id
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def get_sale_by_id(saleId, db):
    return db.query(SaleModel).get(saleId)

def update_sale_in_db(saleId, sale_data, db, current_user_id):
    sale = get_sale_by_id(saleId, db)
    if sale:
        for key, value in sale_data.items():
            setattr(sale, key, value)
        sale.user_id = current_user_id
        db.commit()
        db.refresh(sale)
    return sale

def filter_sales(filters, db):
    query = db.query(SaleModel)
    if filters.get('buyer_name'):
        query = query.filter(SaleModel.buyer_name == filters['buyer_name'])
    # Adicione outros filtros
    return query.all()

def delete_sale_repo(saleId, db):
    db.query(SaleModel).filter_by(id=saleId).delete()
    db.commit()

def insert_sale_in_report(sale, db):
    report = ReportModel()
    report.sale_id = sale.id
    report.sale_qtd_sold = sale.quantity_sold
    report.sale_value = sale.total_value
    report.date_created = sale.sale_date
    db.add(report)
    db.commit()

def update_sale_in_report(sale, db):
    report = db.query(ReportModel).filter_by(sale_id=sale.id).first()
    report.sale_qtd_sold = sale.quantity_sold
    report.sale_value = sale.total_value
    report.date_created = sale.sale_date
    db.commit()

def delete_sale_report(id, db):
    db.query(ReportModel).filter_by(sale_id=id).delete()
    db.commit()