# TODO
- [ ] Have thresholds per endpoint
- [ ] Have better styling for HTML report
- [ ] Install with `pip install git+URL` or make repo public and publish to PyPi?

## Description
Compares two or more CSV files (*with Locust results) based on one or multiple columns and outputs an HTML report with the differences.

## Installation
* Clone the repository and execute:
```
pip install .
```

* Or install directly from the remote repository without cloning, by executing:
```
pip install git+https://github.com/dhis2-sre/csvcomparer.git
```

## Usage

Sample Locust CSV results are available in the `data` directory for testing and demo purposes.

* Compare a single column from the current report with the same column from a previous report
```
csvcomparer \
--current data/dhis_stats.csv \
--previous data/previous_dhis_stats.csv \
--column-name 'Average Response Time'
```

* Compare multiple columns from the current report with the same columns on multiple previous/baseline reports, based on a custom threshold percentage
```
csvcomparer \
--current data/dhis_stats.csv \
--previous data/baseline_dhis_stats.csv data/previous_dhis_stats.csv \
--column-name '90%;Average Response Time' \
--threshold 15
```

* See more information for the available options
```
csvcomparer --help
```
