from flask import jsonify
from repositories.castration_repository import (
    create_castration_in_db,
    delete_castration_report, 
    get_castration_by_id as get_castration_by_id_repo, 
    update_castration_in_db, 
    filter_castrations,
    delete_castration_repo,
    insert_castration_in_report,
    update_castration_in_report
)
from .report_service import get_all_financial_reports

def get_castrations(filters, db):
    # Nenhuma validação necessária aqui, apenas filtramos os dados conforme os parâmetros
    return filter_castrations(filters, db)

def create_castration(castration_data, db, current_user_id):
    # Validação: verificar se todos os campos obrigatórios estão presentes
    required_fields = ['animal_name', 'neutering_date', 'clinic_name_or_veterinary_name', 'cost']
    for field in required_fields:
        if field not in castration_data or not castration_data[field]:
            return jsonify({"detail": f"Campo obrigatório '{field}' está ausente ou vazio."}), 400

    # Validação: o custo da castração deve ser um número positivo
    if 'cost' in castration_data and (castration_data['cost'] <= 0):
        return jsonify({"detail": "O custo da castração deve ser um número positivo."}), 400

    # Validação: a data da castração deve estar no formato correto
    try:
        # Tenta converter a data para verificar a validade
        from datetime import datetime
        datetime.strptime(castration_data['neutering_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"detail": "Formato de data inválido. Use 'YYYY-MM-DD'."}), 400
    
    form_data = get_all_financial_reports(db=db, start_date='1977-01-01', end_date=castration_data['neutering_date'])

    money_spent = 0
    money_raised = 0

    for form in form_data:
       money_spent += form.sale_value
       money_raised += form.castration_value

    money = money_spent - money_raised

    if (money - castration_data['cost']) < 0:
        return jsonify({"detail": "Você não pode fazer a castração porque o dinheiro é insuficiente"}), 400

    # Se todas as validações forem bem-sucedidas, cria a castração
    castration = create_castration_in_db(castration_data, db, current_user_id)

    if castration: 
        insert_castration_in_report(castration, db)

    return castration

def get_castration_by_id(castrationId, db):
    # Verificação: a castração existe?
    castration = get_castration_by_id_repo(castrationId, db)
    if not castration:
        return jsonify({"detail": "Castração não encontrada."}), 404

    return castration

def update_castration(castrationId, castration_data, db, current_user_id):
    # Verificação: a castração existe?
    castration = get_castration_by_id_repo(castrationId, db)
    if not castration:
        return jsonify({"detail": "Castração não encontrada."}), 404

    # Validação: verificar se os dados fornecidos são válidos
    if 'cost' in castration_data and castration_data['cost'] <= 0:
        return jsonify({"detail": "O custo da castração deve ser um número positivo."}), 400

    if 'neutering_date' in castration_data:
        try:
            # Tenta converter a data para verificar a validade
            from datetime import datetime
            datetime.strptime(castration_data['neutering_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"detail": "Formato de data inválido. Use 'YYYY-MM-DD'."}), 400
        
    if  castration_data['cost'] > castration.cost:
        form_data = get_all_financial_reports(db=db, start_date='1977-01-01', end_date=datetime.today())

        money_spent = 0
        money_raised = 0

        for form in form_data:
            money_spent += form.sale_value
            money_raised += form.castration_value

        money = (money_spent - money_raised)

        print(money)

        money = (money + castration.cost)

        print(money)

        if (castration_data['cost']) > money:
            return jsonify({"detail": "Você não pode fazer a castração porque o dinheiro é insuficiente"}), 400
    
        # Se as validações forem bem-sucedidas, atualiza a castração
    updated_castration = update_castration_in_db(castrationId, castration_data, db, current_user_id)

    if updated_castration:
        update_castration_in_report(updated_castration, db)
    return updated_castration

def delete_castration(castrationId, db):
    castration = get_castration_by_id_repo(castrationId, db)
    if not castration:
        return jsonify({"detail": "Castração não encontrada."}), 404
    
    delete_castration_report(castrationId, db)
    
    delete_castration_repo(castrationId, db)

    return None
