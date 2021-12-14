import logging
import sys
import pandas as pd


class Validator:
    def __init__(self, diff: pd.Series, threshold: float) -> None:
        self.diff = diff
        self.threshold = threshold

    def _filter_null_results(self) -> list:
        return list(filter(pd.notnull, self.diff))

    def _all_results_below_threshold(self, results) -> bool:
        return all(result <= self.threshold for result in results)

    def _any_result_above_threshold(self, results) -> bool:
        return any(result > self.threshold for result in results)

    def validate(self) -> None:
        logging.info(f'Allowed threshold: {self.threshold}\n')

        filtered_results = self._filter_null_results()

        if self._all_results_below_threshold(filtered_results):
            sys.exit()
        elif self._any_result_above_threshold(filtered_results):
            sys.exit('Some of the requests are above the given threshold factor!')
        else:
            sys.exit('An error occurred!')
