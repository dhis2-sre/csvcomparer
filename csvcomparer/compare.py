import logging
import os.path
import pandas as pd


class Comparer:
    def __init__(self, threshold, current, previous):
        self.threshold = threshold
        self.current = current
        self.previous = previous
        self.tables = []
        self.file_prefix = None
        self.aggregated_results = None
        self.aggregated_diff = pd.Series(dtype=float)

        pd.set_option('precision', 2)

    def _build_comparison_tables(self, current, previous, column_name):
        self.file_prefix = os.path.basename(previous).split('_')[0].capitalize()

        merged_df = pd.merge(
            current,
            pd.read_csv(previous),
            on=['Type', 'Name'],
            how='outer',
            suffixes=('_current', f'_{self.file_prefix}')
        )

        self.aggregated_results.insert(
            len(self.aggregated_results.columns),
            self.file_prefix,
            merged_df[f'{column_name}_{self.file_prefix}']
        )

    def compare(self, column_name):
        current_df = pd.read_csv(self.current)

        self.aggregated_results = current_df[['Type', 'Name', column_name]].rename(
            columns={f'{column_name}': 'Current'}
        )

        for report in self.previous:
            self._build_comparison_tables(current_df, report, column_name)

            diff = ((self.aggregated_results['Current'] / self.aggregated_results[self.file_prefix]) * 100) - 100
            self.aggregated_diff = self.aggregated_diff.append(diff)
            self.aggregated_results.insert(len(self.aggregated_results.columns), f'{self.file_prefix} Diff', diff)

        self.tables.append(dict(title=column_name, body=self.aggregated_results))

        logging.info(f'Comparison for {column_name} column:\n {self.aggregated_results.to_string()}\n\n')
