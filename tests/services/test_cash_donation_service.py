import pytest
from flask import Flask
from types import SimpleNamespace
from unittest.mock import Mock, patch
from services.cash_donation_service import (
    create_cash_donation,
    get_cas_donation_by_id,
    update_cahs_donation,
    delete_cash_donation
)

app = Flask(__name__)

@pytest.fixture
def mock_db():
    return Mock()

def test_create_valid_cash_donation(mock_db):
    with app.app_context():
        data = {"donor_name": "João", "donation_date": "2024-10-10", "quantity": 100.0}
        mock_donation = Mock()

        # Corrigido: patch onde a função é usada (no módulo services)
        with patch("services.cash_donation_service.create_cash_donation_in_db", return_value=mock_donation) as mock_create, \
             patch("services.cash_donation_service.insert_cash_donation_in_report"):
            result = create_cash_donation(data, mock_db, "user-id")
            assert mock_create.called
            assert result == mock_donation


def test_create_cash_donation_missing_field_returns_400(mock_db):
    with app.app_context():
        data = {"donation_date": "2024-10-10", "quantity": 100.0}  # donor_name ausente
        response, status = create_cash_donation(data, mock_db, "user-id")
        assert status == 400

def test_create_cash_donation_negative_quantity_returns_400(mock_db):
    with app.app_context():
        data = {"donor_name": "Maria", "donation_date": "2024-10-10", "quantity": -50.0}
        response, status = create_cash_donation(data, mock_db, "user-id")
        assert status == 400

def test_get_cash_donation_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.cash_donation_service.get_cash_donation_by_id", return_value=None):
            response, status = get_cas_donation_by_id("fake-id", mock_db)
            assert status == 404

def test_update_cash_donation_blocked_if_spent_exceeds_available(mock_db):
    with app.app_context():
        donation = SimpleNamespace(quantity=200.0)
        reports = [SimpleNamespace(donation=300.0, spent_value=250.0)]
        with patch("services.cash_donation_service.get_cash_donation_by_id", return_value=donation), \
             patch("services.cash_donation_service.get_all_financial_reports", return_value=reports):
            data = {"quantity": 40.0}
            response, status = update_cahs_donation("id", data, mock_db, "user-id")
            assert status == 400

def test_delete_cash_donation_blocked_if_spent_exceeds_available(mock_db):
    with app.app_context():
        donation = SimpleNamespace(quantity=150.0)
        reports = [SimpleNamespace(donation=300.0, spent_value=200.0)]
        with patch("services.cash_donation_service.get_cash_donation_by_id", return_value=donation), \
             patch("services.cash_donation_service.get_all_financial_reports", return_value=reports):
            response, status = delete_cash_donation("id", mock_db)
            assert status == 400
