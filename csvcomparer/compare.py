from __future__ import annotations

import logging
import os.path
import sys

import pandas as pd


class Comparer:

    reports_index = ['Name', 'Type']

    def __init__(self, threshold: float, current_report: str, previous_reports: str) -> None:
        self.threshold = threshold
        self.current_report = current_report
        self.previous_reports = previous_reports
        self.tables = []
        self.file_prefix = None
        self.aggregated_results = None
        self.previous_df = None

        pd.set_option('display.precision', 2)

    def _build_comparison_tables(self, report_name: str, column_name: str) -> None:
        self.previous_df = pd.read_csv(report_name)

        self.file_prefix = os.path.basename(report_name).split('_')[0].capitalize()

        self.aggregated_results.insert(
            len(self.aggregated_results.columns),
            self.file_prefix,
            self.previous_df[column_name]
        )

    def _indexes_equal(self, left: pd.DataFrame, right: pd.DataFrame) -> bool:
        return left.set_index(self.reports_index).index.equals(
            right.set_index(self.reports_index).index
        )

    def get_comparison_tables(self) -> list[dict]:
        return self.tables

    def compare(self, column_name: str) -> None:
        current_df = pd.read_csv(self.current_report)

        self.aggregated_results = current_df[['Type', 'Name', column_name]].rename(
            columns={f'{column_name}': 'Current'}
        )

        aggregated_diff = pd.Series(dtype=float)

        for report_name in self.previous_reports:
            self._build_comparison_tables(report_name, column_name)

            if not self._indexes_equal(current_df, self.previous_df):
                logging.error(f'The Current and {self.file_prefix} reports indexes ({self.reports_index}) are not equal.')
                continue

            diff = ((self.aggregated_results['Current'] / self.aggregated_results[self.file_prefix]) * 100) - 100
            aggregated_diff = aggregated_diff.append(diff)
            self.aggregated_results.insert(len(self.aggregated_results.columns), f'{self.file_prefix} Diff', diff)

        self.tables.append(dict(title=column_name, body=self.aggregated_results))

        logging.info(f'Comparison for {column_name} column:\n {self.aggregated_results.to_string()}\n\n')

        return aggregated_diff
