from typing import Optional
from jinja2 import Environment, FileSystemLoader
from .compare import Comparer


class Reporter:
    percentage_format = '{:+.2f}%'

    def __init__(self, comparer: Comparer, output_file: str) -> None:
        self.comparer = comparer
        self.output_file = output_file

    def _highlight_diff(self, value: float) -> Optional[str]:
        if value > self.comparer.threshold:
            return 'background-color: coral'
        elif value < self.comparer.threshold:
            return 'background-color: darkseagreen'
        else:
            return None

    def _apply_styles(self) -> None:
        diff_columns = [col for col in self.comparer.aggregated_results.columns.values if 'Diff' in col]

        columns_format = {col: self.percentage_format for col in diff_columns}

        for table in self.comparer.tables:
            table['body'] = table['body'].style.format(columns_format, na_rep='NaN')
            table['body'] = table['body'].applymap(self._highlight_diff, subset=diff_columns).render()

    def render(self) -> None:
        self._apply_styles()

        template = Environment(loader=FileSystemLoader('templates')).get_template('comparison-template.html')
        html = template.render(tables=self.comparer.tables)

        html_file = open(self.output_file, 'w')
        html_file.write(html)
        html_file.close()
