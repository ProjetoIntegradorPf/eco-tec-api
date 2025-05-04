import pytest
from flask import Flask
from unittest.mock import patch, Mock
from services.misc_expense_service import (
    list_misc_expenses,
    create_misc_expense_service,
    get_misc_expense_service,
    update_misc_expense_service,
    delete_misc_expense_service
)

app = Flask(__name__)

@pytest.fixture
def mock_db():
    return Mock()

def test_list_misc_expenses_returns_filtered_data(mock_db):
    filters = {"description": "água"}
    with patch("services.misc_expense_service.filter_misc_expenses", return_value=["fake-expense"]) as mock_filter:
        result = list_misc_expenses(filters, mock_db)
        mock_filter.assert_called_once_with(filters, mock_db)
        assert result == ["fake-expense"]

def test_create_misc_expense_service_valid(mock_db):
    with app.app_context():
        data = {"description": "Compra de papel", "value": 50.0}
        expense = Mock()
        expense.to_dict.return_value = {"description": "Compra de papel", "value": 50.0}

        with patch("services.misc_expense_service.create_misc_expense", return_value=expense), \
             patch("services.misc_expense_service.insert_misc_expense_in_report"):
            response, status = create_misc_expense_service(data, mock_db)
            assert status == 201
            assert response.get_json()["description"] == "Compra de papel"

def test_create_misc_expense_service_missing_description_returns_400(mock_db):
    with app.app_context():
        data = {"value": 100}
        response, status = create_misc_expense_service(data, mock_db)
        assert status == 400

def test_create_misc_expense_service_invalid_value_returns_400(mock_db):
    with app.app_context():
        data = {"description": "Café", "value": -5}
        response, status = create_misc_expense_service(data, mock_db)
        assert status == 400

def test_get_misc_expense_service_found(mock_db):
    with app.app_context():
        expense = Mock()
        expense.to_dict.return_value = {"description": "Internet", "value": 80}
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=expense):
            response = get_misc_expense_service("123", mock_db)
            assert response.get_json()["description"] == "Internet"

def test_get_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=None):
            response, status = get_misc_expense_service("invalid", mock_db)
            assert status == 404

def test_update_misc_expense_service_success(mock_db):
    with app.app_context():
        updated = Mock()
        updated.to_dict.return_value = {"description": "Luz", "value": 120}
        with patch("services.misc_expense_service.update_misc_expense", return_value=updated), \
             patch("services.misc_expense_service.update_misc_expense_in_report"):
            response = update_misc_expense_service("abc", {"value": 120}, mock_db)
            assert response.get_json()["value"] == 120

def test_update_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.update_misc_expense", return_value=None):
            response, status = update_misc_expense_service("not-found", {"value": 120}, mock_db)
            assert status == 404

def test_delete_misc_expense_service_success(mock_db):
    with app.app_context():
        expense = Mock()
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=expense), \
             patch("services.misc_expense_service.delete_misc_expense_from_report") as mock_del_report, \
             patch("services.misc_expense_service.delete_misc_expense") as mock_del:
            response, status = delete_misc_expense_service("exp-1", mock_db)
            assert status == 204
            assert mock_del_report.called
            assert mock_del.called

def test_delete_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=None):
            response, status = delete_misc_expense_service("unknown", mock_db)
            assert status == 404
