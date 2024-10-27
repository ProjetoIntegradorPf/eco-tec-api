from flask import jsonify
from repositories.sale_repository import (
    create_sale_in_db, 
    get_sale_by_id as get_sale_by_id_repo, 
    update_sale_in_db, 
    filter_sales,
    delete_sale_repo
)

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

    # Se todas as validações forem bem-sucedidas, cria a venda
    return create_sale_in_db(sale_data, db, current_user_id)

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

    # Se as validações forem bem-sucedidas, atualiza a venda
    updated_sale = update_sale_in_db(saleId, sale_data, db, current_user_id)
    return updated_sale


def delete_sale(saleId, db):
    sale = get_sale_by_id_repo(saleId, db)
    if not sale:
        return jsonify({"detail": "Venda não encontrada."}), 404
    
    delete_sale_repo(saleId, db)

    return None
