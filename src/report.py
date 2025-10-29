# report.py
from jinja2 import Template

def render_report(context, template_path="templates/report.html", out_path="out/report.html"):
    html = Template(open(template_path).read()).render(**context)
    open(out_path, "w", encoding="utf-8").write(html)
    return out_path
