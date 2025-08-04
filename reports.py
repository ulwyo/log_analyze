from abc import ABC, abstractmethod
from collections import defaultdict
import json
from datetime import datetime


class Report(ABC):
    @abstractmethod
    def generate(self, file_paths, filter_date=None):
        """Генерирует отчет на основе данных логов"""
        pass


class AverageReport(Report):
    def generate(self, file_paths, filter_date=None):
        headers = ['handler', 'total', 'avg_response_time']

        data = defaultdict(lambda: {'count': 0, 'total_time': 0})

        for file_path in file_paths:
            with open(file_path, 'r') as file:
                for line in file:
                    log_entry = json.loads(line)
                    log_date = log_entry['@timestamp']
                    if filter_date and datetime.strptime(filter_date, "%Y-%m-%d").date() !=  datetime.fromisoformat(log_date).date():
                        continue

                    handler = log_entry['url']
                    response_time = log_entry['response_time']

                    data[handler]['count'] += 1
                    data[handler]['total_time'] += response_time

        report = []
        for endpoint, data in data.items():
            average_time = data['total_time'] / data['count'] if data['count'] > 0 else 0
            report.append([endpoint, data['count'], average_time])

        return headers, report


class UserAgentReport(Report):
    def generate(self, file_paths, filter_date=None):
        return ["Генерация отчета еще не сделана"], []
