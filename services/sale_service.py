from flask import jsonify
from repositories.report_repository import get_all_financial_reports
from repositories.sale_repository import (
    create_sale_in_db,
    delete_sale_report, 
    get_sale_by_id as get_sale_by_id_repo, 
    update_sale_in_db, 
    filter_sales,
    delete_sale_repo,
    insert_sale_in_report,
    update_sale_in_report
)
from datetime import datetime

def get_sales(filters, db):
    # Não é necessária uma validação adicional aqui, apenas filtrar as vendas conforme os parâmetros
    return filter_sales(filters, db)

def create_sale(sale_data, db, current_user_id):
    # Validação: verificar se todos os campos obrigatórios estão presentes
    required_fields = ['buyer_name', 'sale_date', 'quantity_sold', 'total_value']
    for field in required_fields:
        if field not in sale_data or not sale_data[field]:
            return jsonify({"detail": f"Campo obrigatório '{field}' está ausente ou vazio."}), 400
    
    # Validação: a quantidade vendida deve ser um número positivo
    if 'quantity_sold' in sale_data and sale_data['quantity_sold'] <= 0:
        return jsonify({"detail": "A quantidade de tampinhas vendidas deve ser um número positivo."}), 400

    # Validação: o valor total deve ser um número positivo
    if 'total_value' in sale_data and sale_data['total_value'] <= 0:
        return jsonify({"detail": "O valor total da venda deve ser um número positivo."}), 400

    # Validação: a data da venda deve estar no formato correto
    try:
        from datetime import datetime
        datetime.strptime(sale_data['sale_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"detail": "Formato de data inválido. Use 'YYYY-MM-DD'."}), 400
    

    form_data = get_all_financial_reports(db, start_date='1977-01-01', end_date=sale_data['sale_date'])

    number_of_existing_caps = 0
    number_of_caps_sold = 0

    for form in form_data:
       number_of_existing_caps += form.donation
       number_of_caps_sold += form.sale_qtd_sold
       
    number_of_lids = number_of_existing_caps - number_of_caps_sold

    if (number_of_lids - sale_data['quantity_sold']) < 0:
        return jsonify({"detail": "Você não pode vender essa quantidade de tampinhas, pois excede o que você possui"}), 400

    # Se todas as validações forem bem-sucedidas, cria a venda
    sale = create_sale_in_db(sale_data, db, current_user_id)

    if sale:
        insert_sale_in_report(sale, db)
    
    return sale

def get_sale_by_id(saleId, db):
    # Verificação: a venda existe?
    sale = get_sale_by_id_repo(saleId, db)
    if not sale:
        return jsonify({"detail": "Venda não encontrada."}), 404

    return sale

def update_sale(saleId, sale_data, db, current_user_id):
    # Verificação: a venda existe?
    sale = get_sale_by_id_repo(saleId, db)
    if not sale:
        return jsonify({"detail": "Venda não encontrada."}), 404

    # Validação: verificar se os dados fornecidos são válidos
    if 'quantity_sold' in sale_data and sale_data['quantity_sold'] <= 0:
        return jsonify({"detail": "A quantidade de tampinhas vendidas deve ser um número positivo."}), 400

    if 'total_value' in sale_data and sale_data['total_value'] <= 0:
        return jsonify({"detail": "O valor total da venda deve ser um número positivo."}), 400

    if 'sale_date' in sale_data:
        try:
            from datetime import datetime
            datetime.strptime(sale_data['sale_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"detail": "Formato de data inválido. Use 'YYYY-MM-DD'."}), 400

    if sale_data['quantity_sold'] > sale.quantity_sold:
        form_data = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.today())
        print(len(form_data))

        number_of_existing_caps = 0
        number_of_caps_sold = 0

        for form in form_data:
            number_of_existing_caps = (number_of_existing_caps + form.donation)
            number_of_caps_sold = (number_of_caps_sold + form.sale_qtd_sold)
            
        number_of_lids = (number_of_existing_caps - number_of_caps_sold)

        number_of_lids = (number_of_lids + sale.quantity_sold)

        if (sale_data['quantity_sold']) > number_of_lids:
            return jsonify({"detail": "Você não pode vender essa quantidade de tampinhas, pois excede o que você possui"}), 400

    # Se as validações forem bem-sucedidas, atualiza a venda
    updated_sale = update_sale_in_db(saleId, sale_data, db, current_user_id)
    
    if update_sale:
        update_sale_in_report(updated_sale, db)

    return updated_sale


def delete_sale(saleId, db):
    sale = get_sale_by_id_repo(saleId, db)
    if not sale:
        return jsonify({"detail": "Venda não encontrada."}), 404
    
    form_data = get_all_financial_reports(db, start_date='1977-01-01', end_date=datetime.today())

    # Inicialização das contagens
    total_castration = 0
    total_sold_caps = 0

    # Cálculo das tampinhas doadas e vendidas
    for form in form_data:
        total_castration += form.castration_value
        total_sold_caps += form.sale_value

    print(total_sold_caps)
    # Tampinhas restantes atualmente no sistema
    current_sales = total_sold_caps - sale.total_value

    print(current_sales)
    # Verificação final: se a nova quantidade resulta em um valor menor do que as vendidas
    if (current_sales < total_castration):
        return jsonify({"detail": "Você não pode excluir, pois seu saldo ficará negativo."}), 400
    
    delete_sale_report(saleId, db)

    delete_sale_repo(saleId, db)

    return None
