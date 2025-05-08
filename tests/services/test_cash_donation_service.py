import pytest
from flask import Flask
from types import SimpleNamespace
from unittest.mock import Mock, patch
from services.cash_donation_service import (
    create_cash_donation,
    get_cash_donation_by_id,
    update_cash_donation,
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
            response, status = get_cash_donation_by_id("fake-id", mock_db)
            assert status == 404
