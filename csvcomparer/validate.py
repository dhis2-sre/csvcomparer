import sys
import pandas as pd


class Validator:
    def __init__(self, comparison, results):
        self.comparison = comparison
        self.results = results

    def validate(self):
        print(f'Allowed threshold: {self.comparison.threshold}\n')

        print(self.results)

        if all(result <= self.comparison.threshold for result in self.results.array if pd.notnull(result)):
            sys.exit()
        elif any(result > self.comparison.threshold for result in self.results.array if pd.notnull(result)):
            sys.exit('Some of the requests are above the given threshold factor!')
        else:
            sys.exit('An error occurred!')
