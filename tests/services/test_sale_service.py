import pytest
from flask import Flask
from unittest.mock import patch, Mock
from types import SimpleNamespace
from services.sale_service import (
    create_sale,
    get_sale_by_id,
    update_sale,
    delete_sale
)

app = Flask(__name__)

@pytest.fixture
def mock_db():
    return Mock()

def test_create_sale_valid(mock_db):
    with app.app_context():
        data = {
            "buyer_name": "Cliente A",
            "sale_date": "2024-10-10",
            "quantity_sold": 100,
            "total_value": 200.0
        }

        reports = [SimpleNamespace(donation=500, sale_qtd_sold=200)]
        mock_sale = Mock()

        with patch("services.sale_service.get_all_financial_reports", return_value=reports), \
             patch("services.sale_service.create_sale_in_db", return_value=mock_sale) as mock_create, \
             patch("services.sale_service.insert_sale_in_report"):
            result = create_sale(data, mock_db, "user-id")
            assert mock_create.called
            assert result == mock_sale

def test_create_sale_missing_field_returns_400(mock_db):
    with app.app_context():
        data = {"buyer_name": "Cliente A", "quantity_sold": 100, "total_value": 200.0}  # sale_date faltando
        response, status = create_sale(data, mock_db, "user-id")
        assert status == 400

def test_create_sale_invalid_quantity_returns_400(mock_db):
    with app.app_context():
        data = {"buyer_name": "Cliente A", "sale_date": "2024-10-10", "quantity_sold": -10, "total_value": 100}
        response, status = create_sale(data, mock_db, "user-id")
        assert status == 400

def test_create_sale_insufficient_caps_returns_400(mock_db):
    with app.app_context():
        data = {
            "buyer_name": "Cliente A",
            "sale_date": "2024-10-10",
            "quantity_sold": 600,
            "total_value": 100
        }
        reports = [SimpleNamespace(donation=300, sale_qtd_sold=200)]

        with patch("services.sale_service.get_all_financial_reports", return_value=reports):
            response, status = create_sale(data, mock_db, "user-id")
            assert status == 400

def test_get_sale_by_id_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.sale_service.get_sale_by_id_repo", return_value=None):
            response, status = get_sale_by_id("not-found", mock_db)
            assert status == 404

def test_update_sale_valid(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity_sold=100)
        updated = Mock()
        updated.to_dict = lambda: {"id": "abc", "quantity_sold": 120}
        reports = [SimpleNamespace(donation=500, sale_qtd_sold=350)]

        with patch("services.sale_service.get_sale_by_id_repo", return_value=existing), \
             patch("services.sale_service.get_all_financial_reports", return_value=reports), \
             patch("services.sale_service.update_sale_in_db", return_value=updated) as mock_update, \
             patch("services.sale_service.update_sale_in_report"):
            result = update_sale("abc", {"quantity_sold": 120}, mock_db, "user-id")
            assert mock_update.called
            assert result == updated

def test_update_sale_invalid_quantity_returns_400(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity_sold=100)
        with patch("services.sale_service.get_sale_by_id_repo", return_value=existing):
            response, status = update_sale("abc", {"quantity_sold": 0}, mock_db, "user-id")
            assert status == 400

def test_update_sale_insufficient_caps_returns_400(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity_sold=100)
        reports = [SimpleNamespace(donation=200, sale_qtd_sold=180)]

        with patch("services.sale_service.get_sale_by_id_repo", return_value=existing), \
             patch("services.sale_service.get_all_financial_reports", return_value=reports):
            response, status = update_sale("abc", {"quantity_sold": 300}, mock_db, "user-id")
            assert status == 400

def test_delete_sale_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.sale_service.get_sale_by_id_repo", return_value=None):
            response, status = delete_sale("not-found", mock_db)
            assert status == 404

def test_delete_sale_balance_negative_returns_400(mock_db):
    with app.app_context():
        sale = SimpleNamespace(total_value=300)
        reports = [SimpleNamespace(castration_value=1000, sale_value=700)]  # saldo negativo se excluir

        with patch("services.sale_service.get_sale_by_id_repo", return_value=sale), \
             patch("services.sale_service.get_all_financial_reports", return_value=reports):
            response, status = delete_sale("id", mock_db)
            assert status == 400

def test_delete_sale_success(mock_db):
    with app.app_context():
        sale = SimpleNamespace(total_value=200)
        reports = [SimpleNamespace(castration_value=500, sale_value=800)]

        with patch("services.sale_service.get_sale_by_id_repo", return_value=sale), \
             patch("services.sale_service.get_all_financial_reports", return_value=reports), \
             patch("services.sale_service.delete_sale_report") as mock_del_report, \
             patch("services.sale_service.delete_sale_repo") as mock_del_repo:
            result = delete_sale("id", mock_db)
            assert mock_del_report.called
            assert mock_del_repo.called
            assert result is None
