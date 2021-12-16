import argparse
import logging
import pandas as pd

from .compare import Comparer
from .validate import Validator
from .report import Reporter


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Compare previous Locust run csv report with the current one.'
    )

    parser.add_argument(
        '--loglevel',
        default='error',
        help='Logging level. (default: %(default)s)'
    )

    parser.add_argument(
        '--current',
        required=True,
        type=str,
        help='Current csv report file name to compare with.'
    )

    parser.add_argument(
        '--previous',
        nargs='+',
        required=True,
        type=str,
        help='Previous csv report file name/s to compare to, prefixed with a "string_". (ex. baseline_stats.csv)'
    )

    parser.add_argument(
        '--column-name',
        required=True,
        type=str,
        help='Name of column/s to use for comparison. Can be a semicolon separated list.'
    )

    parser.add_argument(
        '--threshold',
        required=False,
        type=float,
        default=0,
        help='The allowed threshold percentage of difference. (default: %(default)s)'
    )

    parser.add_argument(
        '--output',
        required=False,
        type=str,
        default='comparison-report.html',
        help='HTML report file name. (default: %(default)s)'
    )

    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s:\n%(message)s', level=args.loglevel.upper())

    comparer = Comparer(args.threshold, args.current, args.previous)
    diff = pd.Series(dtype=float)

    for column in args.column_name.split(';'):
        diff = diff.append(comparer.compare(column))

    comparison_tables = comparer.get_comparison_tables()

    reporter = Reporter(comparison_tables, args.threshold, args.output)
    reporter.render()

    validator = Validator(diff, args.threshold)
    validator.validate()


if __name__ == '__main__':
    exit(main())
