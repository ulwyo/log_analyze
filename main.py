import argparse
from tabulate import tabulate

from reports import AverageReport, UserAgentReport


def generate_report(file_path, report_type, filter_date=None):
    report_classes = {
        'average': AverageReport,
        'user_agent': UserAgentReport
    }
    report_class = report_classes.get(report_type)

    if report_class:
        report_instance = report_class()
        return report_instance.generate(file_path, filter_date)
    else:
        raise ValueError("Неизвестный тип отчета")


def main():
    parser = argparse.ArgumentParser(description='Обработка лог-файлов и генерация отчетов')
    parser.add_argument('--file', nargs='+', required=True, help='Путь к файлам логов')
    parser.add_argument('--report', required=True, help='Тип отчета')
    parser.add_argument('--date', type=str, help='Фильтр логов по дате (YYYY-MM-DD)')

    args = parser.parse_args()

    headers, report = generate_report(args.file, args.report, args.date)
    print(
        tabulate(
            report, headers=headers, showindex='always'
        )
    )

if __name__ == '__main__':
    main()
