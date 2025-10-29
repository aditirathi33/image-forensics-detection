# src/main.py
import os, json, pathlib, time, sys, webbrowser
# allow imports when running "python src/main.py ..."
sys.path.append(str(pathlib.Path(__file__).parent))

from hashing import file_hashes
from exif_tools import extract_exif
from ela import make_ela
from copymove import copymove_mask
from jinja2 import Template

def run(image_path):
    project_root = pathlib.Path(__file__).parent.parent  # repo root
    out_dir = project_root / "out"
    tpl_path = project_root / "templates" / "report.html"
    out_dir.mkdir(exist_ok=True)

    p = pathlib.Path(image_path)
    hashes = file_hashes(p)
    exif = extract_exif(str(p))

    # Generate artefacts INTO out/
    ela_file = out_dir / "ela.png"
    cm_file  = out_dir / "copymove_mask.png"
    make_ela(str(p), out_path=str(ela_file))
    copymove_mask(str(p), out_path=str(cm_file))

    # IMPORTANT: Template should reference paths RELATIVE TO report.html location
    # Since report.html will live in out/, use just the filenames:
    context = {
        "file": {"name": p.name, "size": p.stat().st_size},
        "hashes": hashes,
        "exif_json": json.dumps(exif, indent=2),
        "ela_path": ela_file.name,               # "ela.png"
        "copymove_path": cm_file.name,           # "copymove_mask.png"
        "generated_at": time.ctime(),
    }

    # Render HTML
    tpl = tpl_path.read_text(encoding="utf-8")
    html = Template(tpl).render(**context)
    report_path = out_dir / "report.html"
    report_path.write_text(html, encoding="utf-8")
    print(f"Report written to {report_path}")

    # Auto-open in default browser
    webbrowser.open(report_path.resolve().as_uri())

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="Path to the image to analyze")
    args = ap.parse_args()
    run(args.image)
