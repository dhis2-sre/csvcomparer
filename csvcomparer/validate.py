import logging
import sys
import pandas as pd

from .compare import Comparer


class Validator:
    def __init__(self, comparer: Comparer) -> None:
        self.comparer = comparer

    def _filter_null_results(self) -> list:
        return list(filter(pd.notnull, self.comparer.aggregated_diff))

    def _all_results_below_threshold(self, results) -> bool:
        return all(result <= self.comparer.threshold for result in results)

    def _any_result_above_threshold(self, results) -> bool:
        return any(result > self.comparer.threshold for result in results)

    def validate(self) -> None:
        logging.info(f'Allowed threshold: {self.comparer.threshold}\n')

        filtered_results = self._filter_null_results()

        if self._all_results_below_threshold(filtered_results):
            sys.exit()
        elif self._any_result_above_threshold(filtered_results):
            sys.exit('Some of the requests are above the given threshold factor!')
        else:
            sys.exit('An error occurred!')
