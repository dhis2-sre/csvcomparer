import logging
import sys
import pandas as pd


class Validator:
    def __init__(self, comparer, results):
        self.comparer = comparer
        self.results = results

    def _filter_null_results(self):
        return list(filter(pd.notnull, self.results))

    def _all_results_below_threshold(self, results):
        return all(result <= self.comparer.threshold for result in results)

    def _any_result_above_threshold(self, results):
        return any(result > self.comparer.threshold for result in results)

    def validate(self):
        logging.info(f'Allowed threshold: {self.comparer.threshold}\n')

        logging.info(self.results)

        filtered_results = self._filter_null_results()

        if self._all_results_below_threshold(filtered_results):
            sys.exit()
        elif self._any_result_above_threshold(filtered_results):
            sys.exit('Some of the requests are above the given threshold factor!')
        else:
            sys.exit('An error occurred!')
