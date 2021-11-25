"""
TODO:
-
"""

import argparse
import pandas as pd
from .compare import Comparer
from .validate import Validator
from .report import Reporter


def main():
    parser = argparse.ArgumentParser(
        description='Compare previous Locust run csv report with the current one.'
    )

    parser.add_argument(
        'previous',
        help='Previous csv report file to compare to.'
    )

    parser.add_argument(
        'current',
        help='Current csv report file to compare with.'
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
        default=1.0,
        help='The allowed threshold factor of difference (default: %(default)s).'
    )

    parser.add_argument(
        '--output',
        required=False,
        type=str,
        default='comparison-report.html',
        help='HTML report file name (default: %(default)s).'
    )

    args = parser.parse_args()

    comparer = Comparer(args.previous, args.current, args.threshold)
    diff = pd.Series([], dtype=float)

    for column in args.column_name.split(';'):
        diff = diff.append(comparer.compare(column))

    reporter = Reporter(comparer, args.output)
    reporter.render()

    validator = Validator(comparer, diff)
    validator.validate()


if __name__ == '__main__':
    exit(main())
