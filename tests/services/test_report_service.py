import pytest
from unittest.mock import patch, Mock
from services.report_service import fetch_all_financial_reports

@pytest.fixture
def mock_db():
    return Mock()

def test_fetch_all_reports_without_dates(mock_db):
    with patch("services.report_service.get_all_financial_reports", return_value=["report1"]) as mock_repo:
        result = fetch_all_financial_reports(mock_db)
        mock_repo.assert_called_once_with(mock_db, start_date=None, end_date=None)
        assert result == ["report1"]

def test_fetch_all_reports_with_valid_dates(mock_db):
    with patch("services.report_service.get_all_financial_reports", return_value=["report2"]) as mock_repo:
        result = fetch_all_financial_reports(mock_db, "2024-01-01", "2024-12-31")
        from datetime import datetime
        mock_repo.assert_called_once_with(
            mock_db,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31)
        )
        assert result == ["report2"]

def test_fetch_all_reports_with_only_start_date(mock_db):
    with patch("services.report_service.get_all_financial_reports", return_value=["report3"]) as mock_repo:
        result = fetch_all_financial_reports(mock_db, "2023-05-01", None)
        from datetime import datetime
        mock_repo.assert_called_once_with(
            mock_db,
            start_date=datetime(2023, 5, 1),
            end_date=None
        )
        assert result == ["report3"]

def test_fetch_all_reports_with_only_end_date(mock_db):
    with patch("services.report_service.get_all_financial_reports", return_value=["report4"]) as mock_repo:
        result = fetch_all_financial_reports(mock_db, None, "2023-12-31")
        from datetime import datetime
        mock_repo.assert_called_once_with(
            mock_db,
            start_date=None,
            end_date=datetime(2023, 12, 31)
        )
        assert result == ["report4"]
