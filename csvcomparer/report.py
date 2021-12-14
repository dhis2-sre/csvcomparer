from typing import Optional
from jinja2 import Environment, FileSystemLoader


class Reporter:
    percentage_format = '{:+.2f}%'

    def __init__(self, comparison_tables: list[dict], threshold: float, output_file: str) -> None:
        self.comparison_tables = comparison_tables
        self.threshold = threshold
        self.output_file = output_file

    def _highlight_diff(self, value: float) -> Optional[str]:
        if value > self.threshold:
            return 'background-color: coral'
        elif value < self.threshold:
            return 'background-color: darkseagreen'
        else:
            return None

    def _filter_diff_columns(self) -> list:
        columns = []

        for table in self.comparison_tables:
            for column in table['body'].columns.values:
                if 'Diff' in column:
                    columns.append(column)

        return list(set(columns))

    def _apply_styles(self) -> None:
        diff_columns = self._filter_diff_columns()

        columns_format = {col: self.percentage_format for col in diff_columns}

        for table in self.comparison_tables:
            table['body'] = table['body'].style.format(columns_format, na_rep='NaN')
            table['body'] = table['body'].applymap(self._highlight_diff, subset=diff_columns).render()

    def render(self) -> None:
        self._apply_styles()

        template = Environment(loader=FileSystemLoader('templates')).get_template('comparison-template.html')
        html = template.render(tables=self.comparison_tables)

        html_file = open(self.output_file, 'w')
        html_file.write(html)
        html_file.close()
