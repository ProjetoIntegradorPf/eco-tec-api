import pytest
from flask import Flask
from unittest.mock import patch, Mock
from types import SimpleNamespace
from services.donation_service import (
    create_donation,
    get_donation_by_id,
    update_donation,
    delete_donation
)

app = Flask(__name__)

@pytest.fixture
def mock_db():
    return Mock()

def test_create_donation_valid(mock_db):
    with app.app_context():
        data = {"donor_name": "João", "donation_date": "2024-10-10", "quantity": 100}
        mock_donation = Mock()

        with patch("services.donation_service.create_donation_in_db", return_value=mock_donation) as mock_create, \
             patch("services.donation_service.insert_donation_in_report"):
            result = create_donation(data, mock_db, "user-id")
            assert mock_create.called
            assert result == mock_donation

def test_create_donation_missing_field_returns_400(mock_db):
    with app.app_context():
        data = {"donation_date": "2024-10-10", "quantity": 100}  # Falta donor_name
        response, status = create_donation(data, mock_db, "user-id")
        assert status == 400

def test_create_donation_negative_quantity_returns_400(mock_db):
    with app.app_context():
        data = {"donor_name": "João", "donation_date": "2024-10-10", "quantity": -10}
        response, status = create_donation(data, mock_db, "user-id")
        assert status == 400

def test_get_donation_by_id_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.donation_service.get_donation_by_id_repo", return_value=None):
            response, status = get_donation_by_id("invalid-id", mock_db)
            assert status == 404

def test_update_donation_valid(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity=100)
        reports = [SimpleNamespace(donation=300, sale_qtd_sold=150)]
        updated = Mock()
        updated.to_dict.return_value = {
            "id": "some-id",
            "donor_name": "João",
            "donation_date": "2024-10-10",
            "quantity": 120
        }


        with patch("services.donation_service.get_donation_by_id_repo", return_value=existing), \
             patch("services.donation_service.get_all_financial_reports", return_value=reports), \
             patch("services.donation_service.update_donation_in_db", return_value=updated) as mock_update, \
             patch("services.donation_service.update_donation_in_report"):
            result, status = update_donation("id", {"quantity": 120}, mock_db, "user-id")
            assert status == 200
            assert mock_update.called

def test_update_donation_invalid_quantity_returns_400(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity=100)
        with patch("services.donation_service.get_donation_by_id_repo", return_value=existing):
            response, status = update_donation("id", {"quantity": -10}, mock_db, "user-id")
            assert status == 400

def test_update_donation_insufficient_caps_returns_400(mock_db):
    with app.app_context():
        existing = SimpleNamespace(quantity=100)
        reports = [SimpleNamespace(donation=200, sale_qtd_sold=180)]  # vendido > disponível

        with patch("services.donation_service.get_donation_by_id_repo", return_value=existing), \
             patch("services.donation_service.get_all_financial_reports", return_value=reports):
            response, status = update_donation("id", {"quantity": 10}, mock_db, "user-id")
            assert status == 400

def test_delete_donation_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.donation_service.get_donation_by_id_repo", return_value=None):
            response, status = delete_donation("id", mock_db)
            assert status == 404

def test_delete_donation_insufficient_caps_returns_400(mock_db):
    with app.app_context():
        donation = SimpleNamespace(quantity=100)
        reports = [SimpleNamespace(donation=200, sale_qtd_sold=190)]  # vendido > disponível após exclusão

        with patch("services.donation_service.get_donation_by_id_repo", return_value=donation), \
             patch("services.donation_service.get_all_financial_reports", return_value=reports):
            response, status = delete_donation("id", mock_db)
            assert status == 400

def test_delete_donation_valid(mock_db):
    with app.app_context():
        donation = SimpleNamespace(quantity=50)
        reports = [SimpleNamespace(donation=200, sale_qtd_sold=100)]

        with patch("services.donation_service.get_donation_by_id_repo", return_value=donation), \
             patch("services.donation_service.get_all_financial_reports", return_value=reports), \
             patch("services.donation_service.delete_donation_report") as mock_del_report, \
             patch("services.donation_service.delete_donation_repo") as mock_del_repo:
            result = delete_donation("id", mock_db)
            assert mock_del_report.called
            assert mock_del_repo.called
            assert result is None
