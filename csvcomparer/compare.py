import pandas as pd


class Comparer:
    percentage_format = '{:+.2f}%'

    def __init__(self, threshold, current, baseline, previous=None):
        self.threshold = threshold
        self.current = current
        self.baseline = baseline
        self.previous = previous
        self.tables = []

    def compare(self, column_name):
        current_df = pd.read_csv(self.current)
        baseline_df = pd.read_csv(self.baseline)

        current_to_baseline_df = pd.merge(
            current_df,
            baseline_df,
            on=['Type', 'Name'],
            how='outer',
            suffixes=('_current', '_baseline')
        )

        baseline_comparison = current_to_baseline_df[['Type', 'Name', f'{column_name}_baseline', f'{column_name}_current']]
        baseline = baseline_comparison.rename(columns={f'{column_name}_baseline': 'Baseline', f'{column_name}_current': 'Current'})
        baseline_diff = ((baseline['Current'] / baseline['Baseline']) * 100) - 100

        if self.previous is not None:
            previous_df = pd.read_csv(self.previous)

            current_to_previous_df = pd.merge(
                current_df,
                previous_df,
                on=['Type', 'Name'],
                how='outer',
                suffixes=('_current', '_previous')
            )

            previous_comparison = current_to_previous_df[['Type', 'Name', f'{column_name}_previous', f'{column_name}_current']]
            previous = previous_comparison.rename(columns={f'{column_name}_previous': 'Previous', f'{column_name}_current': 'Current'})
            previous_diff = ((previous['Current'] / previous['Previous']) * 100) - 100

        # baseline_and_previous = pd.concat([baseline_comparison, previous_comparison], axis=1)
        baseline_and_previous = baseline
        baseline_and_previous.insert(len(baseline.columns), 'Previous', previous['Previous'])
        compared_columns = baseline_and_previous[['Type', 'Name', 'Baseline', 'Previous', 'Current']]
        compared_columns.insert(len(compared_columns.columns), 'Baseline Diff', baseline_diff)
        compared_columns.insert(len(compared_columns.columns), 'Previous Diff', previous_diff)
        results = compared_columns.style.format({
            'Baseline Diff': self.percentage_format.format,
            'Previous Diff': self.percentage_format.format
        })
        results.applymap(lambda x: 'color: red' if (x > self.threshold) else None, subset=['Baseline Diff', 'Previous Diff'])
        self.tables.append(dict(title=column_name, body=results.render()))

        comparison_table_string = compared_columns.to_string(formatters={"Diff": self.percentage_format.format})

        print(f'Comparison for {column_name} column:\n {comparison_table_string}\n\n')

        merged_diff = baseline_diff.append(previous_diff)

        return merged_diff.add_prefix(f'({column_name})_')
