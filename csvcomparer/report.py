from typing import Optional
from jinja2 import Environment, FileSystemLoader
from .compare import Comparer


class Reporter:
    percentage_format = '{:+.2f}%'

    def __init__(self, comparer: Comparer, output_file: str) -> None:
        self.comparer = comparer
        self.output_file = output_file

    def _highlight_regression(self, value: float) -> Optional[str]:
        return 'color: red' if (value > self.comparer.threshold) else None

    def _apply_styles(self) -> None:
        diff_columns = [col for col in self.comparer.aggregated_results.columns.values if 'Diff' in col]

        columns_format = {col: self.percentage_format for col in diff_columns}

        for table in self.comparer.tables:
            table.update((k, v.style.format(columns_format, na_rep='NaN')) for k, v in table.items() if k == 'body')
            table.update((k, v.applymap(self._highlight_regression, subset=diff_columns).render()) for k, v in table.items() if k == 'body')

    def render(self) -> None:
        self._apply_styles()

        template = Environment(loader=FileSystemLoader('templates')).get_template('comparison-template.html')
        html = template.render(tables=self.comparer.tables)

        html_file = open(self.output_file, 'w')
        html_file.write(html)
        html_file.close()
