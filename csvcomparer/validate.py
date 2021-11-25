import sys


class Validator:
    def __init__(self, comparison, results):
        self.comparison = comparison
        self.results = results

    def validate(self):
        print(f'Threshold factor: {self.comparison.threshold}\n')

        if all(result <= self.comparison.threshold for result in self.results.array):
            sys.exit()
        elif any(result > self.comparison.threshold for result in self.results.array):
            sys.exit('Some of the requests are above the given threshold factor!')
        else:
            sys.exit('An error occurred!')
