import pytest
from flask import Flask
from unittest.mock import Mock, patch
from types import SimpleNamespace
from services.castration_service import (
    create_castration,
    get_castration_by_id,
    update_castration,
    delete_castration
)

app = Flask(__name__)

@pytest.fixture
def mock_db():
    return Mock()

def test_create_castration_valid(mock_db):
    with app.app_context():
        data = {
            "animal_name": "Bidu",
            "neutering_date": "2024-10-10",
            "clinic_name_or_veterinary_name": "Clínica Pet",
            "cost": 100.0
        }

        reports = [SimpleNamespace(sale_value=300.0, castration_value=100.0)]
        mock_castration = Mock()

        with patch("services.castration_service.get_all_financial_reports", return_value=reports), \
             patch("services.castration_service.create_castration_in_db", return_value=mock_castration) as mock_create, \
             patch("services.castration_service.insert_castration_in_report"):
            result = create_castration(data, mock_db, "user-id")
            assert mock_create.called
            assert result == mock_castration

def test_create_castration_missing_field_returns_400(mock_db):
    with app.app_context():
        data = {
            "animal_name": "Bidu",
            "neutering_date": "2024-10-10",
            "cost": 100.0  # faltando clinic_name_or_veterinary_name
        }
        response, status = create_castration(data, mock_db, "user-id")
        assert status == 400

def test_create_castration_invalid_date_returns_400(mock_db):
    with app.app_context():
        data = {
            "animal_name": "Bidu",
            "neutering_date": "10-10-2024",  # formato errado
            "clinic_name_or_veterinary_name": "Vet",
            "cost": 100.0
        }
        response, status = create_castration(data, mock_db, "user-id")
        assert status == 400

def test_create_castration_insufficient_funds_returns_400(mock_db):
    with app.app_context():
        data = {
            "animal_name": "Bidu",
            "neutering_date": "2024-10-10",
            "clinic_name_or_veterinary_name": "Vet",
            "cost": 500.0
        }
        reports = [SimpleNamespace(sale_value=100.0, castration_value=50.0)]
        with patch("services.castration_service.get_all_financial_reports", return_value=reports):
            response, status = create_castration(data, mock_db, "user-id")
            assert status == 400

def test_get_castration_by_id_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.castration_service.get_castration_by_id_repo", return_value=None):
            response, status = get_castration_by_id("invalid-id", mock_db)
            assert status == 404

def test_update_castration_valid(mock_db):
    with app.app_context():
        existing = SimpleNamespace(cost=100.0)
        reports = [SimpleNamespace(sale_value=300.0, castration_value=150.0)]
        updated = Mock()
        with patch("services.castration_service.get_castration_by_id_repo", return_value=existing), \
             patch("services.castration_service.get_all_financial_reports", return_value=reports), \
             patch("services.castration_service.update_castration_in_db", return_value=updated) as mock_update, \
             patch("services.castration_service.update_castration_in_report"):
            result = update_castration("id", {"cost": 150.0}, mock_db, "user-id")
            assert mock_update.called
            assert result == updated

def test_update_castration_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.castration_service.get_castration_by_id_repo", return_value=None):
            response, status = update_castration("id", {"cost": 100.0}, mock_db, "user-id")
            assert status == 404

def test_update_castration_invalid_cost_returns_400(mock_db):
    with app.app_context():
        existing = SimpleNamespace(cost=100.0)
        with patch("services.castration_service.get_castration_by_id_repo", return_value=existing):
            response, status = update_castration("id", {"cost": -50.0}, mock_db, "user-id")
            assert status == 400

def test_delete_castration_not_found_returns_404(mock_db):
    with app.app_context():
        with patch("services.castration_service.get_castration_by_id_repo", return_value=None):
            response, status = delete_castration("id", mock_db)
            assert status == 404

def test_delete_castration_valid(mock_db):
    with app.app_context():
        existing = Mock()
        with patch("services.castration_service.get_castration_by_id_repo", return_value=existing), \
             patch("services.castration_service.delete_castration_report") as mock_del_report, \
             patch("services.castration_service.delete_castration_repo") as mock_del_repo:
            result = delete_castration("id", mock_db)
            assert mock_del_report.called
            assert mock_del_repo.called
            assert result is None
