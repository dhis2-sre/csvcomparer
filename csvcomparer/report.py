from jinja2 import Environment, FileSystemLoader


class Reporter:
    def __init__(self, comparer, output_file):
        self.comparer = comparer
        self.output_file = output_file

    def render(self):
        template = Environment(loader=FileSystemLoader('templates')).get_template("comparison-template.html")
        html = template.render(tables=self.comparer.tables)
        html_file = open(self.output_file, "w")
        html_file.write(html)
        html_file.close()
