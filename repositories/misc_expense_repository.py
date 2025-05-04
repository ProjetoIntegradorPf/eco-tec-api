from models.misc_expense_model import MiscExpenseModel
from models.report_model import ReportModel

def create_misc_expense(expense_data, db):
    expense = MiscExpenseModel(**expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_misc_expense_by_id(expense_id, db):
    return db.query(MiscExpenseModel).get(expense_id)

def update_misc_expense(expense_id, expense_data, db):
    expense = get_misc_expense_by_id(expense_id, db)
    if expense:
        for key, value in expense_data.items():
            if value is not None:
                setattr(expense, key, value)
        db.commit()
        return expense
    return None

def delete_misc_expense(expense_id, db):
    db.query(MiscExpenseModel).filter_by(id=expense_id).delete()
    db.commit()

def filter_misc_expenses(filters, db):
    query = db.query(MiscExpenseModel)
    if filters.get('description'):
        query = query.filter(MiscExpenseModel.description.ilike(f"%{filters['description']}%"))
    if filters.get('expense_date'):
        query = query.filter(MiscExpenseModel.expense_date == filters['expense_date'])
    return query.all()

def insert_misc_expense_in_report(expense, db):
    report = ReportModel()
    report.misc_expense_id = expense.id
    report.misc_expense_value = expense.value
    report.date_created = expense.expense_date
    db.add(report)
    db.commit()

def update_misc_expense_in_report(expense, db):
    report = db.query(ReportModel).filter_by(misc_expense_id=expense.id).first()
    if report:
        report.misc_expense_value = expense.value
        report.date_created = expense.expense_date
        db.commit()

def delete_misc_expense_from_report(expense_id, db):
    db.query(ReportModel).filter_by(misc_expense_id=expense_id).delete()
    db.commit()
