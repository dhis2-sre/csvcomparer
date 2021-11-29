import os.path
import pandas as pd


class Comparer:
    percentage_format = '{:+.2f}%'

    def __init__(self, threshold, current, previous):
        self.threshold = threshold
        self.current = current
        self.previous = previous
        self.tables = []
        self.aggregated_results = None
        self.aggregated_diff = pd.Series(dtype=float)

        pd.set_option('precision', 2)

    def compare(self, column_name):
        current_df = pd.read_csv(self.current)

        self.aggregated_results = current_df[['Type', 'Name', column_name]].rename(
            columns={f'{column_name}': 'Current'}
        )

        for report in self.previous:
            previous_df = pd.read_csv(report)
            file_prefix = os.path.basename(report).split('_')[0].capitalize()

            merged_df = pd.merge(
                current_df,
                previous_df,
                on=['Type', 'Name'],
                how='outer',
                suffixes=('_current', f'_{file_prefix}')
            )

            self.aggregated_results.insert(
                len(self.aggregated_results.columns),
                file_prefix,
                merged_df[f'{column_name}_{file_prefix}']
            )

            diff = ((self.aggregated_results['Current'] / self.aggregated_results[file_prefix]) * 100) - 100
            self.aggregated_diff = self.aggregated_diff.append(diff)
            self.aggregated_results.insert(len(self.aggregated_results.columns), f'{file_prefix} Diff', diff)

        diff_columns = [col for col in self.aggregated_results.columns.values if 'Diff' in col]

        columns_format = {}
        for col in diff_columns:
            columns_format[col] = self.percentage_format

        styled_results = self.aggregated_results.style.format(columns_format, na_rep='NaN')
        styled_results.applymap(lambda x: 'color: red' if (x > self.threshold) else None, subset=diff_columns)

        self.tables.append(dict(title=column_name, body=styled_results.render()))

        comparison_table_string = self.aggregated_results.to_string()
        print(f'Comparison for {column_name} column:\n {comparison_table_string}\n\n')

        return self.aggregated_diff.add_prefix(f'({column_name})_')
