import pytest
import json
from unittest.mock import mock_open, patch

from main import generate_report
from reports import AverageReport, UserAgentReport


sample_log_data = [
    json.dumps({"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "response_time": 0.02}),
    json.dumps({"@timestamp": "2025-06-22T13:57:42+00:00", "status": 200, "url": "/api/context/...", "response_time": 0.04}),
    json.dumps({"@timestamp": "2025-06-22T13:57:52+00:00", "status": 200, "url": "/api/homeworks/...", "response_time": 0.02})
]

@pytest.fixture
def mock_file():
    m = mock_open(read_data='\n'.join(sample_log_data))
    with patch('builtins.open', m):
        yield m


def test_generate_report_average(mock_file):
    headers, report = generate_report(['dummy_path'], 'average')

    assert headers == ['handler', 'total', 'avg_response_time']
    assert report == [
        ["/api/context/...", 2, pytest.approx(0.03)],
        ["/api/homeworks/...", 1, pytest.approx(0.02)]
    ]

def test_generate_report_user_agent(mock_file):
    headers, report = generate_report(['dummy_path'], 'user_agent')

    assert headers == ["Генерация отчета еще не сделана"]
    assert report == []

def test_generate_report_invalid_type(mock_file):
    with pytest.raises(ValueError, match="Неизвестный тип отчета"):
        generate_report(['dummy_path'], 'invalid_report')

def test_average_report(mock_file):
    report = AverageReport()
    headers, data = report.generate(['dummy_path'])

    assert headers == ['handler', 'total', 'avg_response_time']
    assert data == [
        ["/api/context/...", 2, 0.03],
        ["/api/homeworks/...", 1, 0.02]
    ]

def test_user_agent_report(mock_file):
    report = UserAgentReport()
    headers, data = report.generate(['dummy_path'])

    assert headers == ["Генерация отчета еще не сделана"]
    assert data == []
