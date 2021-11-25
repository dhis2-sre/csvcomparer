from jinja2 import Environment, FileSystemLoader


class Reporter:
    def __init__(self, comparison, output_file):
        self.comparison = comparison
        self.output_file = output_file

    def render(self):
        template = Environment(loader=FileSystemLoader('data')).get_template("comparison-template.html")
        html = template.render(tables=self.comparison.tables)
        html_file = open(self.output_file, "w")
        html_file.write(html)
        html_file.close()
