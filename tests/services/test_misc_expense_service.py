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

@ pytest.fixture
def mock_db():
    return Mock()


def test_list_misc_expenses_calls_repository(mock_db):
    # Deve chamar filter_miscenses apenas com o db
    with patch("services.misc_expense_service.filter_misc_expenses", return_value=["fake-expense"]) as mock_filter:
        result = list_misc_expenses(mock_db)
        mock_filter.assert_called_once_with(mock_db)
        assert result == ["fake-expense"]


def test_create_misc_expense_service_valid_calls_repos_and_returns_expense(mock_db):
    data = {"description": "Compra de papel", "value": 50.0}
    expense = Mock()
    with patch("services.misc_expense_service.create_misc_expense", return_value=expense) as mock_create, \
         patch("services.misc_expense_service.insert_misc_expense_in_report") as mock_insert:
        result = create_misc_expense_service(data, mock_db)
        mock_create.assert_called_once_with(data, mock_db)
        mock_insert.assert_called_once_with(expense, mock_db)
        assert result == expense


def test_create_misc_expense_service_missing_description_returns_400(mock_db):
    with app.app_context():
        data = {"value": 100}
        response, status = create_misc_expense_service(data, mock_db)
        assert status == 400
        assert "Campo obrigatório 'description'" in response.get_json()["detail"]


def test_create_misc_expense_service_invalid_value_returns_400(mock_db):
    with app.app_context():
        data = {"description": "Café", "value": -5}
        response, status = create_misc_expense_service(data, mock_db)
        assert status == 400


def test_get_misc_expense_service_found(mock_db):
    expense = Mock()
    with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=expense) as mock_get:
        result = get_misc_expense_service("123", mock_db)
        mock_get.assert_called_once_with("123", mock_db)
        assert result == expense


def test_get_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=None):
            response, status = get_misc_expense_service("invalid", mock_db)
            assert status == 404
            assert "Despesa não encontrada" in response.get_json()["detail"]


def test_update_misc_expense_service_success(mock_db):
    updated = Mock()
    with patch("services.misc_expense_service.update_misc_expense", return_value=updated) as mock_update, \
         patch("services.misc_expense_service.update_misc_expense_in_report") as mock_update_report:
        result = update_misc_expense_service("abc", {"value": 120}, mock_db)
        mock_update.assert_called_once_with("abc", {"value": 120}, mock_db)
        mock_update_report.assert_called_once_with(updated, mock_db)
        assert result == updated


def test_update_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.update_misc_expense", return_value=None):
            response, status = update_misc_expense_service("not-found", {"value": 120}, mock_db)
            assert status == 404
            assert "Despesa não encontrada" in response.get_json()["detail"]


def test_delete_misc_expense_service_success(mock_db):
    expense = Mock()
    with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=expense) as mock_get, \
         patch("services.misc_expense_service.delete_misc_expense_from_report") as mock_del_report, \
         patch("services.misc_expense_service.delete_misc_expense") as mock_del:
        result = delete_misc_expense_service("exp-1", mock_db)
        mock_get.assert_called_once_with("exp-1", mock_db)
        mock_del_report.assert_called_once_with("exp-1", mock_db)
        mock_del.assert_called_once_with("exp-1", mock_db)
        assert result is None


def test_delete_misc_expense_service_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.misc_expense_service.get_misc_expense_by_id", return_value=None):
            response, status = delete_misc_expense_service("unknown", mock_db)
            assert status == 404
            assert "Despesa não encontrada" in response.get_json()["detail"]
