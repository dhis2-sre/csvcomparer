import pandas as pd


class Comparer:
    percentage_format = '{:+.2f}%'

    def __init__(self, previous, current, threshold):
        self.previous = previous
        self.current = current
        self.threshold = threshold
        self.tables = []

    def compare(self, column_name):
        new_df = pd.read_csv(self.current)
        old_df = pd.read_csv(self.previous)

        merged_df = pd.merge(new_df, old_df, on=['Type', 'Name'], how='outer', suffixes=('_new', '_old'))
        compared_columns = merged_df[['Type', 'Name', f'{column_name}_old', f'{column_name}_new']]
        diff = ((compared_columns[f'{column_name}_new'] / compared_columns[f'{column_name}_old']) * 100) - 100

        compared_columns.insert(len(compared_columns.columns), 'Diff', diff)
        results = compared_columns.style.format({'Diff': self.percentage_format.format})
        results.applymap(lambda x: 'color: red' if (x > self.threshold) else None, subset='Diff')
        self.tables.append(dict(title=column_name, body=results.render()))

        comparison_table_string = compared_columns.to_string(formatters={"Diff": self.percentage_format.format})

        print(f'Comparison for {column_name} column:\n {comparison_table_string}\n\n')

        return diff.add_prefix(f'({column_name})_')
